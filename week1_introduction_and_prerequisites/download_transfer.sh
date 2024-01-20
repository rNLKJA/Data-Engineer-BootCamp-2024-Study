#!/bin/bash

python3 dataset_to_postgres_parquet.py \
    --table_name 'yellow_taxi_trip' \
    --user 'root' \
    --password 'root' \
    --host 'localhost' \
    --port 5432 \
    --database 'ny_taxi' \
    --download_path "./data" \
    --year 2021 \
    --start_month 1 \
    --end_month 2 