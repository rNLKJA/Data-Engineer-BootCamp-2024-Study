"""
Data validation utilities for batch processing
Checks data quality before and after transformations.
"""

import pandas as pd
from typing import Dict, Any


def validate_raw_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate raw taxi data and return quality metrics

    Returns dict with:
    - total_rows: total record count
    - null_counts: nulls per column
    - invalid_fares: rows with fare <= 0
    - invalid_distances: rows with distance <= 0
    - data_quality_score: percentage of valid records
    """
    metrics = {
        "total_rows": len(df),
        "null_counts": df.isnull().sum().to_dict(),
        "invalid_fares": len(df[df["fare_amount"] <= 0]),
        "invalid_distances": len(df[df["trip_distance"] <= 0]),
    }

    # Calculate quality score
    invalid_total = metrics["invalid_fares"] + metrics["invalid_distances"]
    valid_rows = metrics["total_rows"] - invalid_total
    metrics["data_quality_score"] = (valid_rows / metrics["total_rows"]) * 100

    return metrics


def validate_transformed_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate transformed data

    Checks:
    - Required columns exist (pickup_year, pickup_month, revenue)
    - No negative revenue
    - Date ranges make sense
    """
    required_cols = ["pickup_year", "pickup_month", "revenue"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    metrics = {
        "total_rows": len(df),
        "negative_revenue": len(df[df["revenue"] < 0]),
        "year_range": (int(df["pickup_year"].min()), int(df["pickup_year"].max())),
        "month_range": (int(df["pickup_month"].min()), int(df["pickup_month"].max())),
        "total_revenue": float(df["revenue"].sum()),
        "avg_revenue": float(df["revenue"].mean()),
    }

    return metrics


def print_validation_report(raw_metrics: Dict, clean_metrics: Dict) -> None:
    """Print a formatted validation report"""
    print("\n" + "=" * 80)
    print("Data Validation Report")
    print("=" * 80)

    print(f"\nRaw Data:")
    print(f"  Total rows: {raw_metrics['total_rows']:,}")
    print(f"  Invalid fares: {raw_metrics['invalid_fares']:,}")
    print(f"  Invalid distances: {raw_metrics['invalid_distances']:,}")
    print(f"  Quality score: {raw_metrics['data_quality_score']:.2f}%")

    print(f"\nTransformed Data:")
    print(f"  Valid rows: {clean_metrics['total_rows']:,}")
    print(f"  Negative revenue: {clean_metrics['negative_revenue']:,}")
    print(f"  Year range: {clean_metrics['year_range']}")
    print(f"  Month range: {clean_metrics['month_range']}")
    print(f"  Total revenue: ${clean_metrics['total_revenue']:,.2f}")
    print(f"  Avg revenue: ${clean_metrics['avg_revenue']:.2f}")

    print("=" * 80)
