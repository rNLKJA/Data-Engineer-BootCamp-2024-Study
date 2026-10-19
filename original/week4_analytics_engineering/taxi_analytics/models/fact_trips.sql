{{
    config(
        materialized='table'
    )
}}

WITH trips AS (
    SELECT * FROM {{ ref('stg_yellow_trips') }}
)

SELECT
    trip_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    pickup_location_id,
    dropoff_location_id,

    -- Calculate revenue
    fare_amount + COALESCE(extra, 0) + COALESCE(mta_tax, 0) +
    COALESCE(tip_amount, 0) + COALESCE(tolls_amount, 0) +
    COALESCE(improvement_surcharge, 0) AS revenue,

    -- Extract date parts for analysis
    DATE_TRUNC('month', pickup_datetime) AS pickup_month,
    EXTRACT(YEAR FROM pickup_datetime) AS pickup_year,
    EXTRACT(MONTH FROM pickup_datetime) AS pickup_month_num,
    EXTRACT(DOW FROM pickup_datetime) AS pickup_day_of_week,

    vendor_id,
    payment_type

FROM trips
