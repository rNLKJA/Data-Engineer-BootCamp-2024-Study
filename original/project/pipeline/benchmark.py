"""Measure what partitioning and clustering buy for representative queries.

Two layouts of the same ``fct_crashes`` rows, both with 8,192-row row groups:

* ``flat``: one unpartitioned Parquet file in REPORT_ID order (no clustering),
  written here as the baseline.
* ``curated``: the dbt export in ``lake/curated/fct_crashes``, partitioned by
  ``crash_year`` and sorted by ``crash_month, lga_name, severity_code``.

The queries are representative, not ones the pipeline runs: two year-bounded
versions of the dashboard tiles (as a year filter or a reload of the latest
release would run them) and a council drill-down. The dbt reporting models that
feed the dashboard aggregate every year from the DuckDB table instead, and this
module is the only reader of the partitioned copy.

For each query and layout this reports the files DuckDB opened (from EXPLAIN
ANALYZE), and the row groups whose min/max statistics could hold a matching
row, i.e. the row groups a reader cannot skip. At about 200,000 rows every
query runs in milliseconds either way; the point is how much data is skipped,
which is what would cost money on a scanned-bytes warehouse.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path

import duckdb

from pipeline.config import Settings, load_settings

ROW_GROUP_SIZE = 8192


@dataclass(frozen=True)
class Predicate:
    column: str
    low: object
    high: object

    def overlaps(self, stats_min: object, stats_max: object) -> bool:
        if stats_min is None or stats_max is None:
            return True
        return not (stats_max < self.low or stats_min > self.high)


@dataclass(frozen=True)
class DashboardQuery:
    name: str
    description: str
    sql: str
    predicates: tuple[Predicate, ...]
    years: tuple[int, int] | None = None  # crash_year bounds, if the query has them
    extra: dict = field(default_factory=dict)


QUERIES = (
    DashboardQuery(
        name="tile2_monthly_fsi_2021_2025",
        description="Representative: Tile 2 for the latest release window, monthly FSI crashes 2021-2025",
        sql=(
            "select crash_month, count(*) filter (where is_fsi) as fsi_crashes from {src} "
            "where crash_year between 2021 and 2025 group by crash_month order by crash_month"
        ),
        predicates=(Predicate("crash_month", dt.date(2021, 1, 1), dt.date(2025, 12, 1)),),
        years=(2021, 2025),
    ),
    DashboardQuery(
        name="tile1_crash_type_fsi_2024",
        description="Representative: Tile 1 for one year, FSI crashes by crash type 2024",
        sql=(
            "select crash_type, count(*) as fsi_crashes from {src} "
            "where crash_year = 2024 and severity_code >= 3 group by crash_type order by crash_type"
        ),
        predicates=(
            Predicate("crash_month", dt.date(2024, 1, 1), dt.date(2024, 12, 1)),
            Predicate("severity_code", 3, 4),
        ),
        years=(2024, 2024),
    ),
    DashboardQuery(
        name="lga_drilldown_adelaide_q1_2024",
        description="Representative: council drill-down with no year filter, City of Adelaide Jan-Mar 2024",
        sql=(
            "select crash_month, count(*) as crashes from {src} "
            "where crash_month between date '2024-01-01' and date '2024-03-01' "
            "and lga_name = 'CITY OF ADELAIDE' group by crash_month order by crash_month"
        ),
        predicates=(
            Predicate("crash_month", dt.date(2024, 1, 1), dt.date(2024, 3, 1)),
            Predicate("lga_name", "CITY OF ADELAIDE", "CITY OF ADELAIDE"),
        ),
    ),
)

_YEAR_RE = re.compile(r"crash_year=(\d{4})")
_FILES_RE = re.compile(r"Total Files Read:\s*(\d+)")


def _sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


def write_flat_baseline(con: duckdb.DuckDBPyConnection, settings: Settings) -> Path:
    target = settings.benchmark_dir / "benchmark" / "fct_crashes_flat.parquet"
    target.parent.mkdir(parents=True, exist_ok=True)
    con.execute(
        f"copy (select * from fct_crashes order by crash_id) to '{_sql_path(target)}' "
        f"(format parquet, compression zstd, row_group_size {ROW_GROUP_SIZE})"
    )
    return target


def _typed(column: str, value: str | None) -> object:
    if value is None:
        return None
    if column == "crash_month":
        return dt.date.fromisoformat(value)
    if column in ("severity_code", "crash_year"):
        return int(value)
    return value


def row_group_stats(con: duckdb.DuckDBPyConnection, glob: str, columns: list[str]) -> list[dict]:
    """Per row group: file, row count and min/max of the filter columns."""
    rows = con.execute(
        "select file_name, row_group_id, row_group_num_rows, path_in_schema, stats_min, stats_max "
        f"from parquet_metadata('{glob}') where path_in_schema in ({', '.join('?' for _ in columns)}) "
        "order by file_name, row_group_id",
        columns,
    ).fetchall()
    groups: dict[tuple[str, int], dict] = {}
    for file_name, rg_id, num_rows, column, stats_min, stats_max in rows:
        group = groups.setdefault((file_name, rg_id), {"file": file_name, "rows": num_rows, "stats": {}})
        group["stats"][column] = (_typed(column, stats_min), _typed(column, stats_max))
    return list(groups.values())


def candidate_row_groups(groups: list[dict], query: DashboardQuery, partitioned: bool) -> list[dict]:
    """Row groups that survive partition pruning and min/max statistics."""
    predicates = list(query.predicates)
    if query.years and not partitioned:
        # In the flat file crash_year is an ordinary column with its own statistics.
        predicates.append(Predicate("crash_year", query.years[0], query.years[1]))
    kept = []
    for group in groups:
        if partitioned and query.years:
            match = _YEAR_RE.search(group["file"])
            if match and not (query.years[0] <= int(match.group(1)) <= query.years[1]):
                continue
        if all(p.overlaps(*group["stats"].get(p.column, (None, None))) for p in predicates):
            kept.append(group)
    return kept


def _timed(con: duckdb.DuckDBPyConnection, sql: str, runs: int = 5) -> tuple[list, float]:
    timings = []
    result: list = []
    for _ in range(runs):
        start = time.perf_counter()
        result = con.execute(sql).fetchall()
        timings.append((time.perf_counter() - start) * 1000)
    return result, statistics.median(timings)


def run(settings: Settings | None = None) -> Path:
    settings = settings or load_settings()
    con = duckdb.connect(str(settings.warehouse_path), read_only=True)
    try:
        flat_path = write_flat_baseline(con, settings)
        curated_glob = _sql_path(settings.curated_dir / "fct_crashes" / "*" / "*.parquet")
        layouts = {
            "flat": (f"read_parquet('{_sql_path(flat_path)}')", _sql_path(flat_path), False),
            "curated": (f"read_parquet('{curated_glob}', hive_partitioning=true)", curated_glob, True),
        }
        filter_columns = sorted({p.column for q in QUERIES for p in q.predicates} | {"crash_year"})
        report: dict = {"row_group_size": ROW_GROUP_SIZE, "queries": []}
        for query in QUERIES:
            entry = {"name": query.name, "description": query.description, "layouts": {}}
            results = {}
            for layout, (source, glob, partitioned) in layouts.items():
                sql = query.sql.format(src=source)
                plan = con.execute("explain analyze " + sql).fetchall()[0][1]
                files_read = int(_FILES_RE.search(plan).group(1)) if _FILES_RE.search(plan) else None
                groups = row_group_stats(con, glob, filter_columns)
                kept = candidate_row_groups(groups, query, partitioned)
                files_total = len({g["file"] for g in groups})
                result, median_ms = _timed(con, sql)
                results[layout] = result
                entry["layouts"][layout] = {
                    "files_total": files_total,
                    "files_read": files_read,
                    "row_groups_total": len(groups),
                    "row_groups_to_read": len(kept),
                    "rows_total": sum(g["rows"] for g in groups),
                    "rows_in_row_groups_to_read": sum(g["rows"] for g in kept),
                    "result_rows": len(result),
                    "median_ms": round(median_ms, 2),
                }
                if layout == "curated" and query.years:
                    print(f"\nEXPLAIN ANALYZE ({query.name}, curated layout)\n{plan}")
            entry["same_result"] = results["flat"] == results["curated"]
            report["queries"].append(entry)
    finally:
        con.close()

    print("\nPartitioning and clustering benchmark (same rows, 8,192-row row groups)")
    header = f"{'query':34} {'layout':8} {'files':>9} {'row groups':>12} {'rows to read':>16} {'median ms':>10}"
    print(header)
    print("-" * len(header))
    for entry in report["queries"]:
        for layout, m in entry["layouts"].items():
            files = f"{m['files_read']}/{m['files_total']}"
            groups = f"{m['row_groups_to_read']}/{m['row_groups_total']}"
            rows = f"{m['rows_in_row_groups_to_read']}/{m['rows_total']}"
            print(f"{entry['name']:34} {layout:8} {files:>9} {groups:>12} {rows:>16} {m['median_ms']:>10.2f}")
        print(f"{'':34} same result on both layouts: {entry['same_result']}")
        if not entry["same_result"]:
            raise RuntimeError(f"{entry['name']}: layouts returned different results")

    out = settings.benchmark_dir / "benchmark.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nbenchmark written to {out}")
    return out


if __name__ == "__main__":
    run()
