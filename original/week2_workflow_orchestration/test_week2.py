"""
Tests for week 2 workflow orchestration.

Run with: pytest original/week2_workflow_orchestration/test_week2.py -v
"""

import shutil
from pathlib import Path

import pandas as pd
import pytest

from etl_web_to_lake import download_data, transform_data, load_to_lake, etl_web_to_lake


@pytest.fixture
def temp_dirs(tmp_path):
    """Create temporary directories for testing."""
    download_dir = tmp_path / "downloads"
    data_lake_root = tmp_path / "data_lake"
    download_dir.mkdir()
    data_lake_root.mkdir()
    yield download_dir, data_lake_root
    # Cleanup handled by tmp_path


def test_download_data(temp_dirs):
    """Test downloading a small sample file (Jan 2021)."""
    download_dir, _ = temp_dirs

    # Download Jan 2021 (small file for testing)
    local_path = download_data.fn(year=2021, month=1, download_dir=download_dir)

    assert local_path.exists()
    assert local_path.name == "yellow_tripdata_2021-01.parquet"
    assert local_path.stat().st_size > 0


def test_transform_data(temp_dirs):
    """Test data transformation on a small sample."""
    download_dir, _ = temp_dirs

    # Download and transform Jan 2021
    local_path = download_data.fn(year=2021, month=1, download_dir=download_dir)
    df = transform_data.fn(input_path=local_path)

    # Verify transformations
    assert len(df) > 0
    assert 'tpep_pickup_datetime' in df.columns
    assert 'tpep_dropoff_datetime' in df.columns
    assert str(df['tpep_pickup_datetime'].dtype).startswith('datetime64')
    assert str(df['tpep_dropoff_datetime'].dtype).startswith('datetime64')

    # No nulls in key columns
    assert df['tpep_pickup_datetime'].notna().all()
    assert df['tpep_dropoff_datetime'].notna().all()


def test_load_to_lake(temp_dirs):
    """Test loading data to the data lake."""
    download_dir, data_lake_root = temp_dirs

    # Download and transform
    local_path = download_data.fn(year=2021, month=1, download_dir=download_dir)
    df = transform_data.fn(input_path=local_path)

    # Load to lake
    row_count = load_to_lake.fn(df, year=2021, month=1, data_lake_root=data_lake_root)

    # Verify file structure
    output_path = data_lake_root / "yellow_taxi" / "2021" / "01" / "yellow_tripdata_2021-01.parquet"
    assert output_path.exists()
    assert row_count == len(df)

    # Verify written data
    loaded_df = pd.read_parquet(output_path)
    assert len(loaded_df) == row_count


def test_etl_web_to_lake_flow(temp_dirs):
    """Test the complete ETL flow end-to-end."""
    download_dir, data_lake_root = temp_dirs

    # Run flow for Jan 2021
    row_count = etl_web_to_lake(
        year=2021,
        month=1,
        data_lake_root=data_lake_root,
        download_dir=download_dir
    )

    # Verify output exists
    output_path = data_lake_root / "yellow_taxi" / "2021" / "01" / "yellow_tripdata_2021-01.parquet"
    assert output_path.exists()
    assert row_count > 0

    # Verify data integrity
    df = pd.read_parquet(output_path)
    assert len(df) == row_count
    assert str(df['tpep_pickup_datetime'].dtype).startswith('datetime64')
