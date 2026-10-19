"""
Aggregation utilities for batch processing
Demonstrates various aggregation patterns (groupby, window, ranking).
"""

import pandas as pd
from pathlib import Path


def aggregate_by_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate metrics by pickup location

    Returns DataFrame with:
    - PULocationID
    - trip_count
    - total_revenue
    - avg_distance
    - avg_passengers
    """
    location_stats = (
        df.groupby("PULocationID")
        .agg(
            {
                "VendorID": "count",
                "revenue": "sum",
                "trip_distance": "mean",
                "passenger_count": "mean",
            }
        )
        .rename(
            columns={
                "VendorID": "trip_count",
                "revenue": "total_revenue",
                "trip_distance": "avg_distance",
                "passenger_count": "avg_passengers",
            }
        )
        .round(2)
    )

    return location_stats.reset_index().sort_values("trip_count", ascending=False)


def aggregate_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate metrics by hour of day

    Shows temporal patterns across Q1 2021
    """
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour

    hourly_stats = (
        df.groupby("pickup_hour")
        .agg(
            {
                "VendorID": "count",
                "revenue": ["sum", "mean"],
                "trip_distance": "mean",
            }
        )
        .round(2)
    )

    hourly_stats.columns = [
        "trip_count",
        "total_revenue",
        "avg_revenue",
        "avg_distance",
    ]

    return hourly_stats.reset_index()


def rank_top_routes(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Find most popular routes (PU -> DO pairs)

    Returns top N routes by trip count with revenue metrics
    """
    route_stats = (
        df.groupby(["PULocationID", "DOLocationID"])
        .agg(
            {
                "VendorID": "count",
                "revenue": ["sum", "mean"],
                "trip_distance": "mean",
            }
        )
        .round(2)
    )

    route_stats.columns = [
        "trip_count",
        "total_revenue",
        "avg_revenue",
        "avg_distance",
    ]

    return (
        route_stats.reset_index()
        .sort_values("trip_count", ascending=False)
        .head(top_n)
    )


if __name__ == "__main__":
    # Demo: load processed data and run aggregations
    week5_dir = Path(__file__).parent
    output_path = week5_dir / "output/taxi_processed"

    # Read all partitions
    parquet_files = list(output_path.rglob("*.parquet"))
    if not parquet_files:
        print("No processed data found. Run batch_process.py first.")
        exit(1)

    df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)

    print("=" * 80)
    print("Batch Aggregation Demonstrations")
    print("=" * 80)

    # Location aggregations
    print("\nTop 10 Pickup Locations by Trip Count:")
    location_stats = aggregate_by_location(df)
    print(location_stats.head(10).to_string(index=False))

    # Hourly aggregations
    print("\nHourly Patterns (sample):")
    hourly_stats = aggregate_by_hour(df)
    print(hourly_stats.head(10).to_string(index=False))

    # Top routes
    print("\nTop 10 Routes:")
    route_stats = rank_top_routes(df, top_n=10)
    print(route_stats.to_string(index=False))
