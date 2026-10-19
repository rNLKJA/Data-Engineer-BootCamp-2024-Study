{{
    config(
        materialized='view'
    )
}}

-- Staging model for Green taxi 2019 data (July only for Q4)

SELECT
    lpep_pickup_datetime AS pickup_datetime,
    lpep_dropoff_datetime AS dropoff_datetime,
    PULocationID AS pickup_location_id,
    DOLocationID AS dropoff_location_id,
    'Green' AS service_type
FROM read_parquet('../data/green_2019/green_tripdata_2019-*.parquet')
WHERE EXTRACT(YEAR FROM lpep_pickup_datetime) = 2019
