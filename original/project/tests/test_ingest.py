"""Offline tests for fetching, validating and loading releases into the lake."""

from __future__ import annotations

import zipfile
from pathlib import Path

import duckdb
import pytest

from conftest import FIXTURES, build_zip, copy_fixture_csvs, fixture_manifest, release_with
from pipeline.ingest import (
    ChecksumMismatchError,
    SchemaContractError,
    SourceNotFoundError,
    SourceUnavailableError,
    extract_release,
    fetch_release,
    lake_partitions,
    load_to_lake,
    prune_stale_partitions,
    validate_schema,
    write_release_manifest,
)


def _served_manifest(fake_dit, fixture_zips):
    manifest = fixture_manifest(fixture_zips, url_template=fake_dit.url_template())
    for release in manifest.releases:
        path = release.url.removeprefix(fake_dit.base_url)
        fake_dit.files[path] = fixture_zips[release.release_id].read_bytes()
    return manifest


def _path(fake_dit, release):
    return release.url.removeprefix(fake_dit.base_url)


# --- fetch ---------------------------------------------------------------


def test_fetch_downloads_verifies_and_then_reuses_the_cache(tmp_path, fake_dit, fixture_zips):
    manifest = _served_manifest(fake_dit, fixture_zips)
    release = manifest.releases[0]
    first = fetch_release(release, tmp_path / "landing", backoff_seconds=0)
    assert not first.cached
    assert first.path.read_bytes() == fixture_zips[release.release_id].read_bytes()
    second = fetch_release(release, tmp_path / "landing", backoff_seconds=0)
    assert second.cached
    assert len(fake_dit.requests) == 1


def test_checksum_mismatch_fails_and_leaves_nothing_behind(tmp_path, fake_dit, fixture_zips):
    manifest = _served_manifest(fake_dit, fixture_zips)
    release = release_with(manifest.releases[0], sha256="0" * 64)
    with pytest.raises(ChecksumMismatchError, match="changed upstream"):
        fetch_release(release, tmp_path / "landing", backoff_seconds=0)
    assert list((tmp_path / "landing").iterdir()) == []


def test_cached_file_with_wrong_bytes_is_downloaded_again(tmp_path, fake_dit, fixture_zips):
    manifest = _served_manifest(fake_dit, fixture_zips)
    release = manifest.releases[0]
    landing = tmp_path / "landing"
    landing.mkdir()
    (landing / release.file).write_bytes(b"stale")
    result = fetch_release(release, landing, backoff_seconds=0)
    assert not result.cached and result.sha256 == release.sha256


def test_404_fails_fast_without_retrying(tmp_path, fake_dit, fixture_zips):
    manifest = _served_manifest(fake_dit, fixture_zips)
    release = manifest.releases[0]
    del fake_dit.files[_path(fake_dit, release)]
    with pytest.raises(SourceNotFoundError, match="HTTP 404"):
        fetch_release(release, tmp_path / "landing", retries=3, backoff_seconds=0)
    assert len(fake_dit.requests) == 1


def test_5xx_is_retried_with_backoff_then_gives_up(tmp_path, fake_dit, fixture_zips):
    manifest = _served_manifest(fake_dit, fixture_zips)
    release = manifest.releases[0]
    fake_dit.failures[_path(fake_dit, release)] = [503, 502, 500]
    sleeps: list[float] = []
    with pytest.raises(SourceUnavailableError, match="gave up after 3 attempts"):
        fetch_release(release, tmp_path / "landing", retries=3, backoff_seconds=0.5, sleep=sleeps.append)
    assert len(fake_dit.requests) == 3
    assert sleeps == [0.5, 1.0]


def test_transient_5xx_recovers(tmp_path, fake_dit, fixture_zips):
    manifest = _served_manifest(fake_dit, fixture_zips)
    release = manifest.releases[1]
    fake_dit.failures[_path(fake_dit, release)] = [500]
    result = fetch_release(release, tmp_path / "landing", retries=3, backoff_seconds=0, sleep=lambda _: None)
    assert result.sha256 == release.sha256
    assert len(fake_dit.requests) == 2


def test_unreachable_host_raises_unavailable(tmp_path, fixture_zips):
    manifest = fixture_manifest(fixture_zips, url_template="http://127.0.0.1:9/{package_id}/{resource_id}/{file}")
    with pytest.raises(SourceUnavailableError):
        fetch_release(manifest.releases[0], tmp_path / "landing", retries=2, backoff_seconds=0, timeout=2)


# --- schema contract -------------------------------------------------------


def test_fixture_releases_pass_the_schema_contract(tmp_path, manifest, fixture_zips):
    expected = {
        "fixture_2019": {"crash": 100, "casualty": 73, "units": 208},
        "fixture_2021_2025": {"crash": 100, "casualty": 75, "units": 211},
    }
    for release in manifest.releases:
        csvs = extract_release(fixture_zips[release.release_id], release, tmp_path / "work")
        assert validate_schema(csvs, release) == expected[release.release_id]


def test_missing_column_breaks_the_contract(tmp_path, manifest):
    csv_dir = copy_fixture_csvs(tmp_path / "csv")
    crash = csv_dir / "2019_DATA_SA_Crash.csv"
    crash.write_text(crash.read_text(encoding="utf-8").replace('"Crash Type"', '"Crash Kind"', 1), encoding="utf-8")
    release = manifest.releases[0]
    zip_path = build_zip("2019", tmp_path / "broken.zip", csv_dir)
    csvs = extract_release(zip_path, release, tmp_path / "work")
    with pytest.raises(SchemaContractError, match=r"missing=\['Crash Type'\] unexpected=\['Crash Kind'\]"):
        validate_schema(csvs, release)


def test_crash_outside_release_years_breaks_the_contract(tmp_path, manifest, fixture_zips):
    release = release_with(manifest.releases[0], first_year=2018, last_year=2018)
    csvs = extract_release(fixture_zips["fixture_2019"], release, tmp_path / "work")
    with pytest.raises(SchemaContractError, match="100 crashes outside 2018-2018"):
        validate_schema(csvs, release)


def test_zip_without_casualty_csv_is_rejected(tmp_path, manifest):
    zip_path = tmp_path / "partial.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.write(FIXTURES / "2019_DATA_SA_Crash.csv", "2019_DATA_SA_Crash.csv")
        archive.write(FIXTURES / "2019_DATA_SA_Units.csv", "2019_DATA_SA_Units.csv")
    with pytest.raises(SchemaContractError, match="_DATA_SA_Casualty.csv"):
        extract_release(zip_path, manifest.releases[0], tmp_path / "work")


# --- lake ------------------------------------------------------------------


def _load_all(manifest, fixture_zips, tmp_path: Path) -> Path:
    raw = tmp_path / "lake" / "raw"
    for release in manifest.releases:
        csvs = extract_release(fixture_zips[release.release_id], release, tmp_path / "work")
        validate_schema(csvs, release)
        load_to_lake(csvs, release, raw)
    write_release_manifest(manifest, raw)
    return raw


def _count(raw: Path, table: str, year: int | None = None) -> int:
    pattern = raw / table / (f"year={year}" if year else "*") / "*.parquet"
    return duckdb.sql(f"select count(*) from read_parquet('{pattern}', hive_partitioning=true)").fetchone()[0]


def test_load_writes_hive_partitions_with_lineage(tmp_path, manifest, fixture_zips):
    raw = _load_all(manifest, fixture_zips, tmp_path)
    for table in ("crash", "casualty", "units"):
        assert lake_partitions(raw, table) == [2019, 2023]
        assert sorted(p.name for p in (raw / table / "year=2019").iterdir()) == ["part_0.parquet"]
    assert _count(raw, "crash") == 200
    assert _count(raw, "casualty") == 148
    assert _count(raw, "units") == 419
    rows = duckdb.sql(
        f"""select year, any_value(_release_id), count("Crash Date Time"), min(_as_at)
            from read_parquet('{raw}/crash/*/*.parquet', hive_partitioning=true) group by year order by year"""
    ).fetchall()
    assert rows[0][:3] == (2019, "fixture_2019", 0)  # no timestamp column before 2021
    assert rows[1][:3] == (2023, "fixture_2021_2025", 100)
    assert str(rows[1][3]) == "2026-10-09"


def test_lake_types_are_cast(tmp_path, manifest, fixture_zips):
    raw = _load_all(manifest, fixture_zips, tmp_path)
    described = duckdb.sql(f"describe select * from read_parquet('{raw}/crash/*/*.parquet', hive_partitioning=true)")
    types = {row[0]: row[1] for row in described.fetchall()}
    assert types["Total Fats"] == "INTEGER"
    assert types["ACCLOC_X"] == "DOUBLE"
    assert types["_as_at"] == "DATE"
    assert "Year" not in types  # stored once, as the partition key


def test_reloading_a_release_is_idempotent(tmp_path, manifest, fixture_zips):
    raw = _load_all(manifest, fixture_zips, tmp_path)
    before = sorted(p.relative_to(raw) for p in raw.rglob("*.parquet"))
    _load_all(manifest, fixture_zips, tmp_path)
    after = sorted(p.relative_to(raw) for p in raw.rglob("*.parquet"))
    assert before == after
    assert _count(raw, "crash") == 200


def test_new_extract_replaces_only_its_own_years(tmp_path, manifest, fixture_zips):
    raw = _load_all(manifest, fixture_zips, tmp_path)
    # A revised bundle with half the 2023 crashes (and their child rows).
    csv_dir = copy_fixture_csvs(tmp_path / "revised")
    crash = csv_dir / "2021-2025_DATA_SA_Crash.csv"
    lines = crash.read_bytes().splitlines(keepends=True)
    crash.write_bytes(b"".join(lines[:51]))
    kept = {line.split(b",", 1)[0] for line in lines[1:51]}
    for table in ("Casualty", "Units"):
        path = csv_dir / f"2021-2025_DATA_SA_{table}.csv"
        rows = path.read_bytes().splitlines(keepends=True)
        path.write_bytes(rows[0] + b"".join(r for r in rows[1:] if r.split(b",", 1)[0] in kept))
    bundle = manifest.releases[1]
    zip_path = build_zip("2021-2025", tmp_path / "revised.zip", csv_dir)
    csvs = extract_release(zip_path, bundle, tmp_path / "work")
    validate_schema(csvs, bundle)
    load_to_lake(csvs, bundle, raw)
    assert _count(raw, "crash", 2023) == 50
    assert _count(raw, "crash", 2019) == 100


def test_prune_removes_years_no_release_covers(tmp_path, manifest, fixture_zips):
    raw = _load_all(manifest, fixture_zips, tmp_path)
    stale = raw / "crash" / "year=2011"
    stale.mkdir()
    (stale / "part_0.parquet").write_bytes(b"")
    removed = prune_stale_partitions(manifest, raw)
    assert removed == [stale]
    assert lake_partitions(raw) == [2019, 2023]


def test_release_manifest_is_stored_in_the_lake(tmp_path, manifest, fixture_zips):
    raw = _load_all(manifest, fixture_zips, tmp_path)
    rows = duckdb.sql(
        f"select release_id, first_year, last_year from read_parquet('{raw}/releases/releases.parquet') order by 1"
    ).fetchall()
    assert rows == [("fixture_2019", 2019, 2019), ("fixture_2021_2025", 2021, 2025)]
