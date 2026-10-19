"""
Prefect orchestration flows for NYC TLC data pipeline

Week 2: Workflow Orchestration
Demonstrates Prefect 2.x flow patterns with retries, caching, and scheduling.
"""

from datetime import timedelta
from pathlib import Path
from typing import List

from prefect import flow, task
from prefect.tasks import task_input_hash

from etl_web_to_lake import download_parquet, upload_to_lake


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_month(year: int, month: int, colour: str) -> Path:
    """Extract single month of taxi data (cached for 1 day)"""
    return download_parquet(year, month, colour)


@task(retries=2)
def load_to_lake(file_path: Path, colour: str) -> None:
    """Load parquet to data lake"""
    upload_to_lake(file_path, colour)


@flow(name="etl-web-to-lake")
def etl_web_to_lake_flow(year: int, month: int, colour: str) -> None:
    """Single month ETL flow"""
    file_path = extract_month(year, month, colour)
    load_to_lake(file_path, colour)


@flow(name="etl-parent-flow")
def etl_parent_flow(
    year: int,
    months: List[int],
    colour: str = "yellow",
) -> None:
    """
    Parent flow to backfill multiple months

    Demonstrates Prefect subflow pattern for parallel execution.
    """
    for month in months:
        etl_web_to_lake_flow(year, month, colour)


if __name__ == "__main__":
    # Example: process Jan-Mar 2021 yellow taxi
    etl_parent_flow(2021, [1, 2, 3], "yellow")
