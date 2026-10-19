"""Fetch, validate and land the DIT road crash releases in the Parquet lake.

The functions here are plain Python so they can be unit-tested without Prefect.
``pipeline.flow`` wraps them as Prefect tasks.

Lake layout (Hive-style partitions, one directory per crash year):

    data/lake/raw/crash/year=2012/part_0.parquet
    data/lake/raw/casualty/year=2012/part_0.parquet
    data/lake/raw/units/year=2012/part_0.parquet
    data/lake/raw/releases/releases.parquet      (the manifest, as data)

Loading a release first deletes that release's year directories, so re-running
a load (or loading a newer extract of the same years) is idempotent and never
touches other years.
"""

from __future__ import annotations

import csv
import hashlib
import logging
import shutil
import time
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import duckdb
import requests

from pipeline.sources import Manifest, Release

log = logging.getLogger(__name__)

TABLES = ("crash", "casualty", "units")
MEMBER_SUFFIX = {
    "crash": "_DATA_SA_Crash.csv",
    "casualty": "_DATA_SA_Casualty.csv",
    "units": "_DATA_SA_Units.csv",
}

# Header contract, taken from the DIT metadata PDF and checked against every
# release from 2012 to 2025. Order is not enforced; names are.
CRASH_COLUMNS = (
    "REPORT_ID", "Stats Area", "Suburb", "Postcode", "LGA Name", "Total Units",
    "Total Cas", "Total Fats", "Total SI", "Total MI", "Year", "Month", "Day",
    "Time", "Area Speed", "Position Type", "Horizontal Align", "Vertical Align",
    "Other Feat", "Road Surface", "Moisture Cond", "Weather Cond", "DayNight",
    "Crash Type", "Unit Resp", "Entity Code", "CSEF Severity", "Traffic Ctrls",
    "DUI Involved", "Drugs Involved", "ACCLOC_X", "ACCLOC_Y", "UNIQUE_LOC",
)  # fmt: skip
CRASH_OPTIONAL_COLUMNS = ("Crash Date Time",)  # added to extracts from 2021
CASUALTY_COLUMNS = (
    "REPORT_ID", "UND_UNIT_NUMBER", "CASUALTY_NUMBER", "Casualty Type", "Sex",
    "AGE", "Position In Veh", "Thrown Out", "Injury Extent", "Seat Belt",
    "Helmet", "Hospital",
)  # fmt: skip
UNITS_COLUMNS = (
    "REPORT_ID", "Unit No", "No Of Cas", "Veh Reg State", "Unit Type", "Veh Year",
    "Direction Of Travel", "Sex", "Age", "Lic State", "Licence Class",
    "Licence Type", "Towing", "Unit Movement", "Number Occupants", "Postcode",
    "Rollover", "Fire",
)  # fmt: skip
CONTRACT = {
    "crash": (CRASH_COLUMNS, CRASH_OPTIONAL_COLUMNS),
    "casualty": (CASUALTY_COLUMNS, ()),
    "units": (UNITS_COLUMNS, ()),
}

# Columns cast on the way into the lake. A value that does not parse fails the
# load (strict CAST) rather than silently becoming NULL. Coded columns that hold
# placeholders such as "XXX" (ages, vehicle year) stay as text and are parsed
# with TRY_CAST in dbt staging, where the rule is documented.
INTEGER_COLUMNS = {
    "crash": ("Total Units", "Total Cas", "Total Fats", "Total SI", "Total MI", "Year"),
    "casualty": ("UND_UNIT_NUMBER", "CASUALTY_NUMBER"),
    "units": ("Unit No", "No Of Cas"),
}
DOUBLE_COLUMNS = {"crash": ("ACCLOC_X", "ACCLOC_Y"), "casualty": (), "units": ()}


class IngestError(RuntimeError):
    """Base class for ingestion failures."""


class SourceNotFoundError(IngestError):
    """The release URL returned 404 or 410: DIT removed or renamed the file."""


class SourceUnavailableError(IngestError):
    """The server kept failing (5xx or network errors) after every retry."""


class ChecksumMismatchError(IngestError):
    """The downloaded bytes do not match the pinned size or SHA-256."""


class SchemaContractError(IngestError):
    """A CSV is missing, has unexpected columns, or holds out-of-range years."""


@dataclass(frozen=True)
class FetchResult:
    release_id: str
    path: Path
    sha256: str
    bytes: int
    cached: bool


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _matches_pin(path: Path, release: Release) -> bool:
    return path.stat().st_size == release.bytes and sha256_file(path) == release.sha256


def fetch_release(
    release: Release,
    landing_dir: Path,
    *,
    session: requests.Session | None = None,
    retries: int = 3,
    backoff_seconds: float = 2.0,
    timeout: float = 60.0,
    sleep: Callable[[float], None] = time.sleep,
) -> FetchResult:
    """Download one release zip into ``landing_dir`` and verify it against the pin.

    A file already in the landing zone with the pinned size and checksum is reused
    (this is what the CI cache restores). 404/410 fail at once with
    ``SourceNotFoundError``; 5xx responses and connection errors are retried with
    exponential backoff and then raise ``SourceUnavailableError``.
    """
    landing_dir = Path(landing_dir)
    landing_dir.mkdir(parents=True, exist_ok=True)
    target = landing_dir / release.file
    if target.exists():
        if _matches_pin(target, release):
            return FetchResult(release.release_id, target, release.sha256, release.bytes, True)
        log.warning("%s: cached file does not match the pin, downloading again", release.file)
        target.unlink()

    http = session or requests.Session()
    partial = target.with_name(target.name + ".part")
    last_error = "no attempt made"
    for attempt in range(1, retries + 1):
        try:
            with http.get(release.url, stream=True, timeout=timeout) as response:
                status = response.status_code
                if status in (404, 410):
                    raise SourceNotFoundError(
                        f"{release.release_id}: HTTP {status} for {release.url}. DIT may have "
                        "removed or renamed this resource; check the dataset page and update "
                        "pipeline/sources.yml."
                    )
                if status >= 500:
                    last_error = f"HTTP {status}"
                elif status != 200:
                    raise IngestError(f"{release.release_id}: unexpected HTTP {status} for {release.url}")
                else:
                    with partial.open("wb") as handle:
                        for chunk in response.iter_content(chunk_size=1 << 16):
                            handle.write(chunk)
                    break
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt < retries:
            delay = backoff_seconds * 2 ** (attempt - 1)
            log.warning("%s: attempt %d/%d failed (%s), retrying in %.1fs",
                        release.release_id, attempt, retries, last_error, delay)  # fmt: skip
            sleep(delay)
    else:
        partial.unlink(missing_ok=True)
        raise SourceUnavailableError(
            f"{release.release_id}: gave up after {retries} attempts ({last_error}) for {release.url}"
        )

    size = partial.stat().st_size
    digest = sha256_file(partial)
    if size != release.bytes or digest != release.sha256:
        partial.unlink(missing_ok=True)
        raise ChecksumMismatchError(
            f"{release.release_id}: got {size} bytes sha256={digest}, pinned {release.bytes} "
            f"bytes sha256={release.sha256}. The file changed upstream; review it and update "
            "pipeline/sources.yml on purpose."
        )
    partial.replace(target)
    return FetchResult(release.release_id, target, digest, size, False)


def extract_release(zip_path: Path, release: Release, work_dir: Path) -> dict[str, Path]:
    """Extract the three CSVs of a release into ``work_dir/<release_id>/``.

    Only the expected members are written, under their base names, so a crafted
    archive cannot write outside the work directory.
    """
    out_dir = Path(work_dir) / release.release_id
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    paths: dict[str, Path] = {}
    with zipfile.ZipFile(zip_path) as archive:
        names = [info.filename for info in archive.infolist() if not info.is_dir()]
        for table, suffix in MEMBER_SUFFIX.items():
            matches = [n for n in names if Path(n).name.lower().endswith(suffix.lower())]
            if len(matches) != 1:
                raise SchemaContractError(
                    f"{release.release_id}: expected one *{suffix} in {Path(zip_path).name}, "
                    f"found {matches or 'none'}"
                )
            member = matches[0]
            base = Path(member).name
            if base in ("", ".", "..") or "/" in base or "\\" in base:
                raise SchemaContractError(f"{release.release_id}: unsafe member name {member!r}")
            destination = out_dir / base
            with archive.open(member) as source, destination.open("wb") as sink:
                shutil.copyfileobj(source, sink)
            paths[table] = destination
    return paths


def read_header(path: Path) -> list[str]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle), [])


def _csv(path: Path) -> str:
    escaped = str(path).replace("'", "''")
    return f"read_csv('{escaped}', header=true, all_varchar=true, delim=',', quote='\"')"


def validate_schema(csv_paths: dict[str, Path], release: Release) -> dict[str, int]:
    """Check the header contract and basic row facts; return row counts per table.

    Raises ``SchemaContractError`` when a required column is missing, an unknown
    column appears, REPORT_ID repeats, or a crash falls outside the release years.
    """
    for table in TABLES:
        if table not in csv_paths:
            raise SchemaContractError(f"{release.release_id}: no {table} CSV")
        header = read_header(csv_paths[table])
        required, optional = CONTRACT[table]
        missing = [c for c in required if c not in header]
        unexpected = [c for c in header if c not in required and c not in optional]
        duplicated = sorted({c for c in header if header.count(c) > 1})
        if missing or unexpected or duplicated:
            raise SchemaContractError(
                f"{release.release_id} {table}: missing={missing} unexpected={unexpected} "
                f"duplicated={duplicated}"
            )

    con = duckdb.connect()
    try:
        counts = {
            table: con.execute(f"select count(*) from {_csv(csv_paths[table])}").fetchone()[0]
            for table in TABLES
        }
        crash = _csv(csv_paths["crash"])
        rows, ids, bad_years, min_year, max_year = con.execute(
            f"""select count(*), count(distinct REPORT_ID),
                       count(*) filter (where try_cast("Year" as integer) is null
                                        or cast("Year" as integer) not between ? and ?),
                       min(try_cast("Year" as integer)), max(try_cast("Year" as integer))
                from {crash}""",
            [release.first_year, release.last_year],
        ).fetchone()
    finally:
        con.close()

    if counts["crash"] == 0:
        raise SchemaContractError(f"{release.release_id}: crash CSV has no rows")
    if ids != rows:
        raise SchemaContractError(f"{release.release_id}: REPORT_ID is not unique ({rows} rows, {ids} ids)")
    if bad_years:
        raise SchemaContractError(
            f"{release.release_id}: {bad_years} crashes outside {release.first_year}-"
            f"{release.last_year} (found {min_year}-{max_year})"
        )
    return counts


def _select_sql(table: str, csv_paths: dict[str, Path], release: Release) -> str:
    header = read_header(csv_paths[table])
    required, optional = CONTRACT[table]
    columns = []
    for name in (*required, *optional):
        if table == "crash" and name == "Year":
            continue  # stored once, as the Hive partition key ``year``
        quoted = '"' + name.replace('"', '""') + '"'
        if name not in header:
            expr = "cast(null as varchar)"
        elif name in INTEGER_COLUMNS[table]:
            expr = f"cast(src.{quoted} as integer)"
        elif name in DOUBLE_COLUMNS[table]:
            expr = f"cast(src.{quoted} as double)"
        else:
            expr = f"src.{quoted}"
        columns.append(f"{expr} as {quoted}")
    member = csv_paths[table].name.replace("'", "''")
    lineage = [
        f"'{release.release_id}' as _release_id",
        f"date '{release.as_at.isoformat()}' as _as_at",
        f"'{release.file}!{member}' as _ingested_from",
    ]
    if table == "crash":
        year = 'cast(src."Year" as integer) as year'
        source = f"{_csv(csv_paths[table])} as src"
    else:
        # Child rows take the crash year so all three tables share partitions.
        year = "crash.year as year"
        source = (
            f"{_csv(csv_paths[table])} as src join "
            f'(select REPORT_ID, cast("Year" as integer) as year from {_csv(csv_paths["crash"])}) '
            "as crash using (REPORT_ID)"
        )
    order = '"REPORT_ID"' if table == "crash" else '"REPORT_ID", 2, 3'
    return f"select {', '.join(columns + lineage)}, {year} from {source} order by {order}"


def load_to_lake(csv_paths: dict[str, Path], release: Release, raw_dir: Path) -> dict[str, int]:
    """Write the release into ``raw_dir/<table>/year=YYYY/`` and return rows written.

    Existing partitions for the release years are removed first, which makes the
    load idempotent and lets a newer extract replace only its own years.
    """
    raw_dir = Path(raw_dir)
    written: dict[str, int] = {}
    con = duckdb.connect()
    try:
        for table in TABLES:
            table_dir = raw_dir / table
            for year in release.years:
                shutil.rmtree(table_dir / f"year={year}", ignore_errors=True)
            table_dir.mkdir(parents=True, exist_ok=True)
            target = str(table_dir).replace("'", "''")
            con.execute(
                f"copy ({_select_sql(table, csv_paths, release)}) to '{target}' "
                "(format parquet, compression zstd, partition_by (year), "
                "overwrite_or_ignore true, filename_pattern 'part_{i}')"
            )
            files = [str(p) for year in release.years for p in sorted((table_dir / f"year={year}").glob("*.parquet"))]
            written[table] = (
                con.execute("select count(*) from read_parquet(?)", [files]).fetchone()[0] if files else 0
            )
    finally:
        con.close()
    return written


def prune_stale_partitions(manifest: Manifest, raw_dir: Path) -> list[Path]:
    """Delete year partitions that no release in the manifest covers."""
    keep = {f"year={year}" for year in manifest.years}
    removed = []
    for table in TABLES:
        table_dir = Path(raw_dir) / table
        if not table_dir.exists():
            continue
        for child in sorted(table_dir.iterdir()):
            if child.is_dir() and child.name.startswith("year=") and child.name not in keep:
                shutil.rmtree(child)
                removed.append(child)
    return removed


def write_release_manifest(manifest: Manifest, raw_dir: Path) -> Path:
    """Store the pinned manifest in the lake so dbt tests can check release ranges."""
    target = Path(raw_dir) / "releases" / "releases.parquet"
    target.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    try:
        con.execute(
            "create table releases (release_id varchar, first_year integer, last_year integer, "
            "as_at date, resource_id varchar, file varchar, bytes bigint, sha256 varchar, url varchar)"
        )
        con.executemany(
            "insert into releases values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (r.release_id, r.first_year, r.last_year, r.as_at, r.resource_id, r.file, r.bytes, r.sha256, r.url)
                for r in manifest.releases
            ],
        )
        escaped = str(target).replace("'", "''")
        con.execute(f"copy (select * from releases order by first_year) to '{escaped}' (format parquet)")
    finally:
        con.close()
    return target


def lake_partitions(raw_dir: Path, table: str = "crash") -> list[int]:
    table_dir = Path(raw_dir) / table
    if not table_dir.exists():
        return []
    return sorted(int(p.name.split("=", 1)[1]) for p in table_dir.glob("year=*") if p.is_dir())
