"""
Query optimisation demonstrations with DuckDB
Shows partitioning benefits, EXPLAIN plans, and index strategies.
"""

import duckdb
from pathlib import Path
from time import time


def benchmark_full_scan(con: duckdb.DuckDBPyConnection, data_path: str) -> float:
    """Benchmark full table scan"""
    start = time()
    result = con.execute(
        f"""
        SELECT COUNT(*), SUM(total_amount)
        FROM read_parquet('{data_path}')
    """
    ).fetchone()
    elapsed = time() - start
    print(f"Full scan: {result[0]:,} rows, ${result[1]:,.2f} total | {elapsed:.3f}s")
    return elapsed


def benchmark_partitioned_query(
    con: duckdb.DuckDBPyConnection, partition_path: str
) -> float:
    """Benchmark partitioned query (single month)"""
    start = time()
    result = con.execute(
        f"""
        SELECT COUNT(*), SUM(total_amount)
        FROM read_parquet('{partition_path}')
    """
    ).fetchone()
    elapsed = time() - start
    print(
        f"Partition scan: {result[0]:,} rows, ${result[1]:,.2f} total | {elapsed:.3f}s"
    )
    return elapsed


def show_explain_plans(con: duckdb.DuckDBPyConnection, data_path: str) -> None:
    """Show query plans for comparison"""
    print("\n" + "=" * 80)
    print("EXPLAIN Analysis: Full Scan vs Partition Pruning")
    print("=" * 80)

    # Full scan plan
    print("\nFull Scan Plan:")
    result = con.execute(
        f"""
        EXPLAIN SELECT COUNT(*)
        FROM read_parquet('{data_path}')
    """
    ).fetchall()
    for row in result[:5]:  # First 5 lines
        print(f"  {row[1]}")

    # Partitioned query plan
    jan_path = str(Path(data_path).parent / "2021/01/*.parquet")
    print("\nPartitioned Query Plan (Jan 2021 only):")
    result = con.execute(
        f"""
        EXPLAIN SELECT COUNT(*)
        FROM read_parquet('{jan_path}')
    """
    ).fetchall()
    for row in result[:5]:
        print(f"  {row[1]}")


def demonstrate_clustering_benefits(
    con: duckdb.DuckDBPyConnection, data_path: str
) -> None:
    """
    Demonstrate clustering benefits via sorted writes

    In DuckDB, partitioning by year/month simulates BigQuery's clustering.
    Files written with ORDER BY have better compression and filter performance.
    """
    print("\n" + "=" * 80)
    print("Clustering Simulation (via sorted Parquet writes)")
    print("=" * 80)

    # Query with filter on pickup location (benefits from clustering)
    print("\nQuery with location filter (clustered column):")
    start = time()
    result = con.execute(
        f"""
        SELECT COUNT(*), AVG(trip_distance)
        FROM read_parquet('{data_path}')
        WHERE PULocationID = 132
    """
    ).fetchone()
    elapsed = time() - start
    print(f"  {result[0]:,} trips | avg: {result[1]:.2f} mi | {elapsed:.3f}s")

    print("\nNote: DuckDB's Parquet reader uses statistics for filter pushdown.")
    print("Sorted writes (ORDER BY PULocationID) enable better skip rates.")


if __name__ == "__main__":
    con = duckdb.connect()
    base_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake"
    data_path = base_path / "yellow_taxi/**/*.parquet"
    jan_path = base_path / "yellow_taxi/2021/01/*.parquet"

    print("=" * 80)
    print("Query Optimisation Benchmarks")
    print("=" * 80 + "\n")

    full_time = benchmark_full_scan(con, str(data_path))
    partition_time = benchmark_partitioned_query(con, str(jan_path))

    speedup = full_time / partition_time if partition_time > 0 else 0
    print(f"\nPartition pruning speedup: {speedup:.2f}x")

    show_explain_plans(con, str(data_path))
    demonstrate_clustering_benefits(con, str(data_path))

    con.close()
