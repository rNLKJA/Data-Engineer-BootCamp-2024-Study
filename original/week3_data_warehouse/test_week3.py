"""
Tests for week 3 data warehouse queries.

Run with: pytest original/week3_data_warehouse/test_week3.py -v
"""

import duckdb
from pathlib import Path


def test_week2_data_exists():
    """Verify week 2 data lake exists for querying."""
    data_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi"
    assert data_path.exists(), "Week 2 data lake not found"

    jan_data = data_path / "2021/01"
    assert jan_data.exists(), "January 2021 partition not found"

    parquet_files = list(jan_data.glob("*.parquet"))
    assert len(parquet_files) > 0, "No parquet files found in January 2021 partition"


def test_duckdb_read_parquet():
    """Test DuckDB can read parquet files from data lake."""
    con = duckdb.connect()
    data_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/*.parquet"

    result = con.execute(f"SELECT COUNT(*) FROM read_parquet('{data_path}')").fetchone()
    assert result[0] > 0, "No rows read from parquet"
    con.close()


def test_partition_pruning():
    """Test that querying a single partition reads fewer rows than full scan."""
    con = duckdb.connect()

    # Single partition
    jan_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/*.parquet"
    jan_count = con.execute(f"SELECT COUNT(*) FROM read_parquet('{jan_path}')").fetchone()[0]

    # All partitions
    all_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/**/*.parquet"
    all_count = con.execute(f"SELECT COUNT(*) FROM read_parquet('{all_path}')").fetchone()[0]

    assert jan_count < all_count, "Single partition should have fewer rows than all partitions"
    con.close()


def test_aggregation_queries():
    """Test aggregation queries work correctly."""
    con = duckdb.connect()
    data_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/**/*.parquet"

    # Sum query
    result = con.execute(f"SELECT SUM(trip_distance) FROM read_parquet('{data_path}')").fetchone()
    assert result[0] > 0, "Trip distance sum should be positive"

    # Group by query
    result = con.execute(f"SELECT PULocationID, COUNT(*) FROM read_parquet('{data_path}') GROUP BY PULocationID LIMIT 1").fetchone()
    assert result[1] > 0, "Grouped count should be positive"

    con.close()


def test_explain_query():
    """Test EXPLAIN works for query plans."""
    con = duckdb.connect()
    data_path = Path(__file__).parent / "../week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/*.parquet"

    result = con.execute(f"EXPLAIN SELECT COUNT(*) FROM read_parquet('{data_path}')").fetchall()
    assert len(result) > 0, "EXPLAIN should return query plan"
    con.close()
