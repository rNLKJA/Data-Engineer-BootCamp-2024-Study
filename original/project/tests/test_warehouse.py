"""Integration tests: the real lake and warehouse after `python -m pipeline.flow`."""

from __future__ import annotations

import json

import duckdb
import pytest

from pipeline.ingest import TABLES, lake_partitions
from pipeline.sources import load_manifest

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def con(settings_module):
    if not settings_module.warehouse_path.exists():
        pytest.fail(f"warehouse missing at {settings_module.warehouse_path}; run `python -m pipeline.flow` first")
    connection = duckdb.connect(str(settings_module.warehouse_path), read_only=True)
    yield connection
    connection.close()


@pytest.fixture(scope="module")
def settings_module():
    from pipeline.config import load_settings

    return load_settings()


def _lake_count(settings, table: str) -> int:
    pattern = settings.raw_dir / table / "*" / "*.parquet"
    return duckdb.sql(f"select count(*) from read_parquet('{pattern}', hive_partitioning=true)").fetchone()[0]


def test_lake_has_one_partition_per_year_for_every_table(settings_module):
    years = load_manifest(settings_module.sources_path).years
    assert len(years) == 14
    for table in TABLES:
        assert lake_partitions(settings_module.raw_dir, table) == years


def test_row_counts_carry_through_from_lake_to_warehouse(settings_module, con):
    assert _lake_count(settings_module, "crash") == con.execute("select count(*) from stg_crashes").fetchone()[0]
    assert _lake_count(settings_module, "crash") == con.execute("select count(*) from fct_crashes").fetchone()[0]
    assert _lake_count(settings_module, "casualty") == con.execute("select count(*) from fct_casualties").fetchone()[0]
    assert _lake_count(settings_module, "units") == con.execute("select count(*) from stg_units").fetchone()[0]


def test_lake_counts_match_the_crash_totals(settings_module, con):
    total_cas, total_units = con.execute("select sum(total_cas), sum(total_units) from fct_crashes").fetchone()
    assert _lake_count(settings_module, "casualty") == total_cas
    assert _lake_count(settings_module, "units") == total_units


def test_fct_crashes_is_stored_in_cluster_order(con):
    out_of_order = con.execute(
        """select count(*) from (
               select (crash_month, lga_name, severity_code, crash_id) as k,
                      lag((crash_month, lga_name, severity_code, crash_id)) over (order by rowid) as prev
               from fct_crashes)
           where prev is not null and k < prev"""
    ).fetchone()[0]
    assert out_of_order == 0


def test_curated_export_is_partitioned_with_small_sorted_row_groups(settings_module, con):
    root = settings_module.curated_dir / "fct_crashes"
    partitions = sorted(p.name for p in root.iterdir() if p.is_dir())
    assert partitions == [f"crash_year={y}" for y in range(2012, 2026)]
    meta = duckdb.sql(
        f"""select max(row_group_num_rows), count(distinct (file_name, row_group_id))
            from parquet_metadata('{root}/*/*.parquet')"""
    ).fetchone()
    assert meta[0] <= 8192
    assert meta[1] >= 14
    exported = duckdb.sql(f"select count(*) from read_parquet('{root}/*/*.parquet')").fetchone()[0]
    assert exported == con.execute("select count(*) from fct_crashes").fetchone()[0]


def test_every_dbt_node_passed(settings_module):
    run_results = json.loads((settings_module.dbt_project_dir / "target" / "run_results.json").read_text())
    results = run_results["results"]
    failures = [r["unique_id"] for r in results if r["status"] not in ("success", "pass")]
    assert failures == []
    assert sum(r["unique_id"].startswith("test.") for r in results) >= 60
    assert sum(r["unique_id"].startswith("model.") for r in results) == 13


def test_benchmark_shows_less_data_to_read_on_the_curated_layout(settings_module):
    report = json.loads((settings_module.benchmark_dir / "benchmark.json").read_text())
    assert report["row_group_size"] == 8192
    for query in report["queries"]:
        assert query["same_result"], query["name"]
        flat, curated = query["layouts"]["flat"], query["layouts"]["curated"]
        assert curated["rows_in_row_groups_to_read"] <= flat["rows_in_row_groups_to_read"], query["name"]
    year_bounded = [q for q in report["queries"] if q["layouts"]["curated"]["files_read"] < 14]
    assert len(year_bounded) == 2


def test_lga_aliases_leave_no_trailing_full_stops(con):
    assert con.execute("select count(*) from dim_lga where lga_name like '%.'").fetchone()[0] == 0
    assert con.execute("select count(*) from dim_lga").fetchone()[0] == 72
