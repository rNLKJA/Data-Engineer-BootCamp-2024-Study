"""
ETL pipeline: Download NYC taxi data and load to local data lake (Prefect orchestration).

This flow downloads yellow taxi parquet files from DataTalksClub GitHub releases,
performs light transformation (drop nulls, type casting), and writes partitioned
parquet files to a local data_lake directory (standing in for GCS).
"""

import argparse
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, retry_delay_seconds=10, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def download_data(year: int, month: int, download_dir: Path) -> Path:
    """
    Download NYC yellow taxi parquet file for a given year and month.

    Returns the local file path. Retries 3 times on failure with 10s delay.
    Caches the result for 1 day based on input hash.
    """
    download_dir.mkdir(parents=True, exist_ok=True)
    filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
    local_path = download_dir / filename

    if local_path.exists():
        print(f"File already exists: {local_path}")
        return local_path

    # NYC TLC data from the official source (CloudFront CDN)
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{filename}"

    print(f"Downloading {url} ...")
    response = requests.get(url, timeout=300)
    response.raise_for_status()

    local_path.write_bytes(response.content)
    print(f"Downloaded to {local_path} ({local_path.stat().st_size / 1024 / 1024:.2f} MB)")

    return local_path


@task(log_prints=True)
def transform_data(input_path: Path) -> pd.DataFrame:
    """
    Load parquet file and apply light transformations.

    - Drop rows with null pickup/dropoff datetime
    - Ensure datetime columns are properly typed
    - Return cleaned DataFrame
    """
    df = pd.read_parquet(input_path)
    print(f"Loaded {len(df):,} rows from {input_path.name}")

    # Drop rows with missing key timestamps
    initial_count = len(df)
    df = df.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
    dropped = initial_count - len(df)
    if dropped > 0:
        print(f"Dropped {dropped:,} rows with null pickup/dropoff datetime")

    # Ensure datetime columns are typed correctly
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    print(f"Transformed: {len(df):,} rows ready for load")
    return df


@task(log_prints=True)
def load_to_lake(df: pd.DataFrame, year: int, month: int, data_lake_root: Path) -> int:
    """
    Write DataFrame to partitioned parquet in the data lake.

    File structure: data_lake/yellow_taxi/{year}/{month:02d}/yellow_tripdata_{year}-{month:02d}.parquet
    Returns the number of rows written.
    """
    output_dir = data_lake_root / "yellow_taxi" / str(year) / f"{month:02d}"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"yellow_tripdata_{year}-{month:02d}.parquet"
    df.to_parquet(output_path, index=False, engine='pyarrow')

    print(f"Wrote {len(df):,} rows to {output_path}")
    return len(df)


@flow(name="etl-web-to-lake", log_prints=True)
def etl_web_to_lake(year: int, month: int, data_lake_root: Optional[Path] = None, download_dir: Optional[Path] = None):
    """
    Main ETL flow: download, transform, load NYC yellow taxi data.

    Args:
        year: Year of data (e.g. 2021)
        month: Month of data (1-12)
        data_lake_root: Root directory for the data lake (default: ./data_lake)
        download_dir: Directory for temporary downloads (default: ./downloads)
    """
    if data_lake_root is None:
        data_lake_root = Path(__file__).parent / "data_lake"
    if download_dir is None:
        download_dir = Path(__file__).parent / "downloads"

    print(f"=== ETL Flow: {year}-{month:02d} ===")

    # Extract
    local_file = download_data(year, month, download_dir)

    # Transform
    df = transform_data(local_file)

    # Load
    row_count = load_to_lake(df, year, month, data_lake_root)

    print(f"=== Flow complete: {row_count:,} rows processed ===")
    return row_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL: download and load NYC yellow taxi data to data lake")
    parser.add_argument("--year", type=int, required=True, help="Year (e.g. 2021)")
    parser.add_argument("--month", type=int, required=True, help="Month (1-12)")
    parser.add_argument("--data-lake-root", type=Path, default=None, help="Data lake root directory")
    parser.add_argument("--download-dir", type=Path, default=None, help="Download directory")

    args = parser.parse_args()

    etl_web_to_lake(
        year=args.year,
        month=args.month,
        data_lake_root=args.data_lake_root,
        download_dir=args.download_dir
    )
