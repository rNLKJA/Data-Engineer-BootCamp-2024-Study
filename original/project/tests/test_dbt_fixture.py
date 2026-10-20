"""Offline end-to-end check: the fixture slice goes through the lake and dbt.

Builds a lake from the 200-crash fixture in a temporary directory and runs
`dbt build` against a temporary DuckDB file, so every model and data test is
exercised without the network. The full_data tag marks tests that only make
sense on the complete release set.
"""

from __future__ import annotations

import json

import duckdb

from conftest import FIXTURE_RELEASES
from pipeline.dbt_runner import run_dbt
from pipeline.ingest import extract_release, load_to_lake, validate_schema, write_release_manifest


def test_dbt_build_passes_on_the_fixture(tmp_path, monkeypatch, manifest, fixture_zips, settings):
    lake = tmp_path / "lake"
    for release in manifest.releases:
        csvs = extract_release(fixture_zips[release.release_id], release, tmp_path / "work")
        validate_schema(csvs, release)
        load_to_lake(csvs, release, lake / "raw")
    write_release_manifest(manifest, lake / "raw")
    (lake / "curated").mkdir()

    warehouse = tmp_path / "fixture.duckdb"
    monkeypatch.setenv("SA_CRASH_LAKE", str(lake))
    monkeypatch.setenv("SA_CRASH_WAREHOUSE", str(warehouse))
    target = tmp_path / "dbt_target"
    outcome = run_dbt(
        [
            "build",
            "--project-dir", str(settings.dbt_project_dir),
            "--profiles-dir", str(settings.dbt_profiles_dir),
            "--target-path", str(target),
            "--log-path", str(tmp_path / "dbt_logs"),
            "--exclude", "tag:full_data",
        ]  # fmt: skip
    )
    assert outcome.success, outcome.exception

    run_results = json.loads((target / "run_results.json").read_text())
    statuses = {r["status"] for r in run_results["results"]}
    assert statuses <= {"success", "pass"}
    assert sum(r["unique_id"].startswith("test.") for r in run_results["results"]) >= 50

    con = duckdb.connect(str(warehouse), read_only=True)
    try:
        assert con.execute("select count(*) from fct_crashes").fetchone()[0] == 200
        assert con.execute("select count(*) from fct_casualties").fetchone()[0] == 148
        by_severity = dict(con.execute("select severity_code, count(*) from fct_crashes group by 1").fetchall())
        assert by_severity == {1: 80, 2: 60, 3: 40, 4: 20}
        # The month spine spans the fixture releases' full year range (2019-2025).
        first, last, months = con.execute(
            "select min(crash_month), max(crash_month), count(*) from rpt_monthly_severity"
        ).fetchone()
        first_year = min(r["first_year"] for r in FIXTURE_RELEASES)
        assert (first.year, first.month, last.year, last.month) == (first_year, 1, 2025, 12)
        assert months == (2025 - first_year + 1) * 12
        assert con.execute("select sum(fsi_crashes) from rpt_crash_type_severity").fetchone()[0] == 60
    finally:
        con.close()
    assert sorted(p.name for p in (lake / "curated" / "fct_crashes").iterdir()) == [
        "crash_year=2019",
        "crash_year=2023",
    ]
