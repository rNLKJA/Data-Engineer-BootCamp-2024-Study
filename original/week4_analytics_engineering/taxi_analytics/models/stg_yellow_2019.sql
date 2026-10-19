{{
    config(
        materialized='view'
    )
}}

-- Staging model for Yellow taxi 2019 data (July only for Q4)

SELECT
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,
    PULocationID AS pickup_location_id,
    DOLocationID AS dropoff_location_id,
    'Yellow' AS service_type
FROM read_parquet('../data/yellow_2019/yellow_tripdata_2019-*.parquet')
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2019
