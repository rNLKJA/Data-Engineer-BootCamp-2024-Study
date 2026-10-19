"""
Backfill script: run ETL flow for a range of months.

Example:
    python backfill.py --year 2021 --start-month 1 --end-month 3
"""

import argparse
from pathlib import Path

from etl_web_to_lake import etl_web_to_lake


def backfill(year: int, start_month: int, end_month: int, data_lake_root: Path = None, download_dir: Path = None):
    """
    Run ETL flow for each month in the range [start_month, end_month].

    Each flow run is tracked separately by Prefect.
    """
    total_rows = 0

    for month in range(start_month, end_month + 1):
        print(f"\n{'='*60}")
        print(f"Backfilling: {year}-{month:02d}")
        print(f"{'='*60}\n")

        row_count = etl_web_to_lake(year, month, data_lake_root, download_dir)
        total_rows += row_count

    print(f"\n{'='*60}")
    print(f"Backfill complete: {total_rows:,} total rows processed across {end_month - start_month + 1} months")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill ETL flow for a range of months")
    parser.add_argument("--year", type=int, required=True, help="Year (e.g. 2021)")
    parser.add_argument("--start-month", type=int, required=True, help="Start month (1-12)")
    parser.add_argument("--end-month", type=int, required=True, help="End month (1-12)")
    parser.add_argument("--data-lake-root", type=Path, default=None, help="Data lake root directory")
    parser.add_argument("--download-dir", type=Path, default=None, help="Download directory")

    args = parser.parse_args()

    backfill(
        year=args.year,
        start_month=args.start_month,
        end_month=args.end_month,
        data_lake_root=args.data_lake_root,
        download_dir=args.download_dir
    )
