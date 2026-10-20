"""Cut the small real-data test fixture from the landed DIT zips.

Picks a stratified, deterministic sample of crashes (ordered by MD5 of
REPORT_ID) from the 2019 release and from 2023 in the 2021-2025 release, then
keeps every casualty and unit row belonging to those crashes. Source lines are
copied byte for byte so the fixture keeps DIT's quoting and CRLF endings.
Run after `make ingest`:

    python scripts/make_fixtures.py data/landing tests/fixtures
"""

from __future__ import annotations

import csv
import hashlib
import sys
import zipfile
from pathlib import Path

# (zip file, member prefix, year to keep, crashes per CSEF severity code)
PLAN = (
    ("2019_data_sa_as_at_20210527.zip", "2019", "2019", {"1": 40, "2": 30, "3": 20, "4": 10}),
    ("2021-2025_data_sa_crash_as_at_20261009.zip", "2021-2025", "2023", {"1": 40, "2": 30, "3": 20, "4": 10}),
)
TABLES = ("Crash", "Casualty", "Units")


def _lines(archive: zipfile.ZipFile, name: str) -> tuple[bytes, list[str], list[tuple[bytes, list[str]]]]:
    """Return the raw header line, parsed header, and (raw line, parsed row) pairs."""
    raw_lines = archive.read(name).splitlines(keepends=True)
    header = next(csv.reader([raw_lines[0].decode("utf-8-sig")]))
    rows = []
    for raw in raw_lines[1:]:
        parsed = next(csv.reader([raw.decode("utf-8")]))
        if len(parsed) != len(header):
            raise ValueError(f"{name}: a record spans lines; line filtering is unsafe")
        rows.append((raw, parsed))
    return raw_lines[0], header, rows


def main(landing: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for zip_name, prefix, year, quota in PLAN:
        with zipfile.ZipFile(landing / zip_name) as archive:
            _, header, crashes = _lines(archive, f"{prefix}_DATA_SA_Crash.csv")
            idx = {name: i for i, name in enumerate(header)}
            rows = [p for _, p in crashes if p[idx["Year"]] == year]
            rows.sort(key=lambda p: hashlib.md5(p[idx["REPORT_ID"]].encode()).hexdigest())
            keep: set[str] = set()
            for code, count in quota.items():
                picked = [p for p in rows if p[idx["CSEF Severity"]].startswith(code + ":")][:count]
                keep.update(p[idx["REPORT_ID"]] for p in picked)
            for table in TABLES:
                head_raw, head, body = _lines(archive, f"{prefix}_DATA_SA_{table}.csv")
                id_col = head.index("REPORT_ID")
                selected = [raw for raw, parsed in body if parsed[id_col] in keep]
                target = out_dir / f"{prefix}_DATA_SA_{table}.csv"
                target.write_bytes(head_raw + b"".join(selected))
                print(f"{target.name}: {len(selected)} rows")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
