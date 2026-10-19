"""
DuckDB warehouse queries demonstrating partitioning, clustering, and optimization.

Run from week3_data_warehouse directory after week 2 data is loaded.
"""

import duckdb
from pathlib import Path


def main():
    # Connect to DuckDB (in-memory)
    con = duckdb.connect()

    # Path to week 2 data lake
    data_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/**/*.parquet"

    print("="*80)
    print("Week 3: Data Warehouse Queries with DuckDB")
    print("="*80)

    # Path to specific partition for Q1
    jan_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/*.parquet"

    # ===== Question 1: Row count for January 2021 =====
    print("\n[Q1] Row count for January 2021:")
    result = con.execute(f"""
        SELECT COUNT(*) as row_count
        FROM read_parquet('{jan_path}')
    """).fetchone()
    print(f"     {result[0]:,} rows")

    # ===== Question 2: Total trip distance for Q1 2021 =====
    print("\n[Q2] Total trip distance for Q1 2021 (Jan, Feb, Mar):")
    result = con.execute(f"""
        SELECT SUM(trip_distance) as total_distance
        FROM read_parquet('{data_path}')
    """).fetchone()
    print(f"     {result[0]:,.2f} miles")

    # ===== Question 6: Compare full scan vs partitioned query =====
    print("\n[Q6a] Full scan EXPLAIN (all partitions):")
    result = con.execute(f"""
        EXPLAIN SELECT COUNT(*)
        FROM read_parquet('{data_path}')
    """).fetchall()
    for row in result:
        print(f"     {row[1]}")

    print("\n[Q6b] Partitioned query EXPLAIN (only Jan 2021):")
    result = con.execute(f"""
        EXPLAIN SELECT COUNT(*)
        FROM read_parquet('{jan_path}')
    """).fetchall()
    for row in result:
        print(f"     {row[1]}")

    # ===== Bonus: Top pickup locations in Q1 2021 =====
    print("\n[Bonus] Top 5 pickup locations in Q1 2021:")
    result = con.execute(f"""
        SELECT PULocationID, COUNT(*) as trip_count
        FROM read_parquet('{data_path}')
        GROUP BY PULocationID
        ORDER BY trip_count DESC
        LIMIT 5
    """).fetchall()
    for row in result:
        print(f"     Location {row[0]}: {row[1]:,} trips")

    # ===== Bonus: Average trip distance per file (showing partition structure) =====
    print("\n[Bonus] Row count per partition (month):")
    result = con.execute(f"""
        SELECT filename, COUNT(*) as row_count
        FROM read_parquet('{data_path}', filename=true)
        GROUP BY filename
        ORDER BY filename
    """).fetchall()
    for row in result:
        month = row[0].split('/')[-2]  # Extract month from path
        print(f"     Month {month}: {row[1]:,} rows")

    print("\n" + "="*80)
    print("All queries complete!")
    print("="*80)

    con.close()


if __name__ == "__main__":
    main()
