{{
    config(
        materialized='view'
    )
}}

-- Staging model for FHV 2019 data
-- Filters to keep only 2019 pickup times
-- No deduplication as per homework instructions

SELECT
    dispatching_base_num,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
    PULocationID AS pickup_location_id,
    DOLocationID AS dropoff_location_id,
    SR_Flag AS shared_ride_flag,
    Affiliated_base_number AS affiliated_base_number,
    'FHV' AS service_type
FROM read_parquet('../data/fhv_2019/fhv_tripdata_2019-*.parquet')
WHERE EXTRACT(YEAR FROM pickup_datetime) = 2019
