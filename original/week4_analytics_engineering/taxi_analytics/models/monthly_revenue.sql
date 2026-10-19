{{
    config(
        materialized='table'
    )
}}

WITH trips AS (
    SELECT * FROM {{ ref('fact_trips') }}
)

SELECT
    pickup_year,
    pickup_month_num,
    pickup_month,

    -- Aggregated metrics
    COUNT(*) AS total_trips,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_revenue_per_trip,
    SUM(trip_distance) AS total_distance,
    AVG(trip_distance) AS avg_distance_per_trip,
    AVG(passenger_count) AS avg_passengers

FROM trips
GROUP BY pickup_year, pickup_month_num, pickup_month
ORDER BY pickup_year, pickup_month_num
