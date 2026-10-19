{{
    config(
        materialized='table'
    )
}}

-- Union of all service types (FHV, Yellow, Green) for July 2019 analysis
-- Combines fact_fhv_trips with yellow and green 2019 staging data

WITH fhv_trips AS (
    SELECT
        pickup_datetime,
        'FHV' AS service_type
    FROM {{ ref('fact_fhv_trips') }}
),

yellow_trips AS (
    SELECT
        pickup_datetime,
        service_type
    FROM {{ ref('stg_yellow_2019') }}
),

green_trips AS (
    SELECT
        pickup_datetime,
        service_type
    FROM {{ ref('stg_green_2019') }}
),

all_trips AS (
    SELECT * FROM fhv_trips
    UNION ALL
    SELECT * FROM yellow_trips
    UNION ALL
    SELECT * FROM green_trips
)

SELECT
    service_type,
    pickup_datetime,
    EXTRACT(YEAR FROM pickup_datetime) AS pickup_year,
    EXTRACT(MONTH FROM pickup_datetime) AS pickup_month
FROM all_trips
