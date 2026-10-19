{{
    config(
        materialized='table'
    )
}}

-- Fact table for FHV trips
-- Joins with dim_zones to get zone names
-- Keeps only records with known pickup and dropoff locations
-- Filters out NULL location IDs and Unknown zones (264, 265)

WITH fhv_trips AS (
    SELECT * FROM {{ ref('stg_fhv_tripdata') }}
    WHERE pickup_location_id IS NOT NULL
      AND dropoff_location_id IS NOT NULL
      AND pickup_location_id NOT IN (264, 265)
      AND dropoff_location_id NOT IN (264, 265)
),

zones AS (
    SELECT
        LocationID,
        Borough,
        Zone,
        service_zone
    FROM read_csv_auto('../data/taxi_zone_lookup.csv')
    WHERE Zone != 'Unknown'
)

SELECT
    fhv.dispatching_base_num,
    fhv.pickup_datetime,
    fhv.dropoff_datetime,
    fhv.pickup_location_id,
    fhv.dropoff_location_id,
    fhv.shared_ride_flag,
    fhv.affiliated_base_number,
    pickup_zone.Borough AS pickup_borough,
    pickup_zone.Zone AS pickup_zone,
    dropoff_zone.Borough AS dropoff_borough,
    dropoff_zone.Zone AS dropoff_zone
FROM fhv_trips fhv
INNER JOIN zones AS pickup_zone
    ON fhv.pickup_location_id = pickup_zone.LocationID
INNER JOIN zones AS dropoff_zone
    ON fhv.dropoff_location_id = dropoff_zone.LocationID
