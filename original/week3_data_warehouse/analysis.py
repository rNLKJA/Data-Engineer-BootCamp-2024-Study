"""
Analytical queries for NYC TLC warehouse
Demonstrates aggregations, window functions, and complex JOINs with DuckDB.
"""

import duckdb
from pathlib import Path


def analyse_pickup_patterns(con: duckdb.DuckDBPyConnection, data_path: str) -> None:
    """Analyse pickup location patterns across Q1 2021"""
    print("\n" + "=" * 80)
    print("Pickup Location Analysis")
    print("=" * 80)

    # Top pickup locations
    result = con.execute(
        f"""
        SELECT
            PULocationID,
            COUNT(*) as trip_count,
            ROUND(AVG(trip_distance), 2) as avg_distance,
            ROUND(AVG(total_amount), 2) as avg_fare
        FROM read_parquet('{data_path}')
        GROUP BY PULocationID
        HAVING trip_count > 1000
        ORDER BY trip_count DESC
        LIMIT 10
    """
    ).fetchall()

    print("\nTop 10 Pickup Locations:")
    for row in result:
        print(
            f"  Location {row[0]:>3}: {row[1]:>8,} trips | "
            f"avg dist: {row[2]:>6.2f} mi | avg fare: ${row[3]:>6.2f}"
        )


def analyse_time_patterns(con: duckdb.DuckDBPyConnection, data_path: str) -> None:
    """Analyse temporal patterns (hourly, daily)"""
    print("\n" + "=" * 80)
    print("Temporal Pattern Analysis")
    print("=" * 80)

    # Trips by hour of day
    result = con.execute(
        f"""
        SELECT
            EXTRACT(HOUR FROM tpep_pickup_datetime) as pickup_hour,
            COUNT(*) as trip_count,
            ROUND(AVG(trip_distance), 2) as avg_distance
        FROM read_parquet('{data_path}')
        GROUP BY pickup_hour
        ORDER BY pickup_hour
    """
    ).fetchall()

    print("\nTrips by Hour of Day (Q1 2021):")
    for row in result:
        print(f"  Hour {row[0]:>2}: {row[1]:>8,} trips | avg: {row[2]:>5.2f} mi")


def analyse_revenue(con: duckdb.DuckDBPyConnection, data_path: str) -> None:
    """Revenue analysis by payment type and trip type"""
    print("\n" + "=" * 80)
    print("Revenue Analysis")
    print("=" * 80)

    # Revenue by payment type
    result = con.execute(
        f"""
        SELECT
            payment_type,
            COUNT(*) as trip_count,
            ROUND(SUM(total_amount), 2) as total_revenue,
            ROUND(AVG(total_amount), 2) as avg_fare
        FROM read_parquet('{data_path}')
        GROUP BY payment_type
        ORDER BY total_revenue DESC
    """
    ).fetchall()

    print("\nRevenue by Payment Type:")
    for row in result:
        print(
            f"  Type {row[0]}: {row[1]:>8,} trips | "
            f"total: ${row[2]:>12,.2f} | avg: ${row[3]:>6.2f}"
        )


if __name__ == "__main__":
    con = duckdb.connect()
    data_path = (
        Path(__file__).parent
        / "../week2_workflow_orchestration/data_lake/yellow_taxi/**/*.parquet"
    )

    analyse_pickup_patterns(con, str(data_path))
    analyse_time_patterns(con, str(data_path))
    analyse_revenue(con, str(data_path))

    con.close()
