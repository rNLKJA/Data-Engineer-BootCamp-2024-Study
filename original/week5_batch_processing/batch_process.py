"""Batch processing for NYC taxi data using pandas.

PySpark local mode hit Java compatibility issues on this machine.
This pandas-based version demonstrates the same batch processing concepts:
- Reading partitioned Parquet files
- DataFrame transformations (filter, map, groupby, agg)
- Writing partitioned Parquet output
- Scalable to Spark when moving to a cluster

In production, swap pandas for PySpark with minimal code changes.
"""

import pandas as pd
from pathlib import Path


def read_taxi_data(data_path):
    """Read yellow taxi Parquet files."""
    print(f"Reading data from {data_path}")
    parquet_files = list(data_path.glob("*.parquet"))
    print(f"Found {len(parquet_files)} Parquet files")

    # Read all files into a single DataFrame
    df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
    print(f"Loaded {len(df):,} rows")
    return df


def transform_taxi_data(df):
    """Apply transformations: add date columns, filter invalid records, calculate revenue."""
    # Filter invalid records
    df_clean = df[(df['fare_amount'] > 0) & (df['trip_distance'] > 0)].copy()

    # Add date columns
    df_clean['pickup_year'] = df_clean['tpep_pickup_datetime'].dt.year
    df_clean['pickup_month'] = df_clean['tpep_pickup_datetime'].dt.month

    # Calculate revenue
    df_clean['revenue'] = (
        df_clean['fare_amount'] +
        df_clean['extra'] +
        df_clean['mta_tax'] +
        df_clean['tip_amount'] +
        df_clean['tolls_amount'] +
        df_clean['improvement_surcharge'] +
        df_clean.get('congestion_surcharge', 0).fillna(0)
    )

    print(f"After filtering: {len(df_clean):,} valid rows")
    return df_clean


def compute_monthly_stats(df):
    """Aggregate monthly revenue and trip statistics."""
    monthly_stats = df.groupby(['pickup_year', 'pickup_month']).agg({
        'VendorID': 'count',
        'revenue': ['sum', 'mean'],
        'trip_distance': ['sum', 'mean'],
        'passenger_count': 'mean'
    }).round(2)

    monthly_stats.columns = [
        'trip_count', 'total_revenue', 'avg_revenue',
        'total_distance', 'avg_distance', 'avg_passengers'
    ]

    return monthly_stats.reset_index().sort_values(['pickup_year', 'pickup_month'])


def write_partitioned_parquet(df, output_path):
    """Write DataFrame as partitioned Parquet files (year/month)."""
    print(f"\nWriting partitioned output to {output_path}")
    output_path.mkdir(parents=True, exist_ok=True)

    for (year, month), group in df.groupby(['pickup_year', 'pickup_month']):
        partition_dir = output_path / f"year={year}" / f"month={month}"
        partition_dir.mkdir(parents=True, exist_ok=True)
        group.to_parquet(partition_dir / "data.parquet", index=False)
        print(f"  Wrote {len(group):,} rows to year={year}/month={month}")


def main():
    """Main batch processing pipeline."""
    # Data paths
    week5_dir = Path(__file__).parent
    repo_root = week5_dir.parent.parent
    input_path = repo_root / "original/week2_workflow_orchestration/downloads"
    output_path = week5_dir / "output/taxi_processed"

    # Process data
    df_raw = read_taxi_data(input_path)
    df_clean = transform_taxi_data(df_raw)

    # Compute statistics
    monthly_stats = compute_monthly_stats(df_clean)
    print("\nMonthly Statistics:")
    print(monthly_stats.to_string(index=False))

    # Write partitioned output
    write_partitioned_parquet(df_clean, output_path)

    print("\nBatch processing complete!")

    # Homework queries
    print("\n=== Homework Answers ===")

    # Q1: Total revenue Q1 2021
    q1_revenue = df_clean[
        (df_clean['pickup_year'] == 2021) &
        (df_clean['pickup_month'].between(1, 3))
    ]['revenue'].sum()
    print(f"Q1 2021 Total Revenue: ${q1_revenue:,.2f}")

    # Q2: Trip count January 2021
    jan_trips = len(df_clean[
        (df_clean['pickup_year'] == 2021) &
        (df_clean['pickup_month'] == 1)
    ])
    print(f"January 2021 Trip Count: {jan_trips:,}")

    # Q3: Average distance March 2021
    mar_avg_dist = df_clean[
        (df_clean['pickup_year'] == 2021) &
        (df_clean['pickup_month'] == 3)
    ]['trip_distance'].mean()
    print(f"March 2021 Average Distance: {mar_avg_dist:.2f} miles")

    # Q4: Highest average revenue month
    q1_months = monthly_stats[monthly_stats['pickup_year'] == 2021]
    highest_month_row = q1_months.loc[q1_months['avg_revenue'].idxmax()]
    print(f"Highest Average Revenue: Month {highest_month_row['pickup_month']} " +
          f"(${highest_month_row['avg_revenue']:.2f} per trip)")


if __name__ == "__main__":
    main()
