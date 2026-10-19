{{
    config(
        materialized='view'
    )
}}

WITH source AS (
    SELECT * FROM read_parquet('/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/downloads/yellow_tripdata_*.parquet')
)

SELECT
    -- Generate unique trip ID
    MD5(CAST(tpep_pickup_datetime AS VARCHAR) || CAST(tpep_dropoff_datetime AS VARCHAR) || CAST(VendorID AS VARCHAR)) AS trip_id,

    -- Timestamps
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,

    -- Trip info
    passenger_count,
    trip_distance,
    PULocationID AS pickup_location_id,
    DOLocationID AS dropoff_location_id,

    -- Payment
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    payment_type,

    -- Metadata
    VendorID AS vendor_id

FROM source
WHERE trip_distance > 0  -- Filter out zero-distance trips
  AND fare_amount > 0    -- Filter out zero-fare trips
