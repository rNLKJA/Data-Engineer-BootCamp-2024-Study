{#
  Curated crash fact. DuckDB has no CLUSTER BY, so clustering is done by
  writing rows in (crash_month, lga_name, severity_code) order: each row group's
  min/max statistics then cover a narrow range and DuckDB can skip row groups
  for month-bounded dashboard queries. The post-hook exports the same rows as
  Parquet partitioned by crash_year with small (8,192-row) row groups, which is
  the layout pipeline/benchmark.py measures.
#}
{{
  config(
    materialized='table',
    post_hook=[
      "copy (select * from {{ this }} order by crash_month, lga_name, severity_code, crash_id)
       to '{{ env_var('SA_CRASH_LAKE') }}/curated/fct_crashes'
       (format parquet, compression zstd, partition_by (crash_year), row_group_size 8192,
        overwrite true, filename_pattern 'part_{i}')"
    ]
  )
}}

with crashes as (
    select * from {{ ref('stg_crashes') }}
),

severity as (
    select * from {{ ref('severity_levels') }}
),

casualty_counts as (
    select * from {{ ref('int_casualty_counts') }}
),

regimes as (
    select * from {{ ref('pdo_reporting_regimes') }}
),

latest as (
    -- The newest year in the data is still being revised by DIT.
    select max(crash_year) as provisional_year from crashes
)

select
    crashes.crash_id,
    crashes.crash_year,
    crashes.crash_month,
    crashes.crash_month_number,
    crashes.day_of_week,
    crashes.crash_hour,
    crashes.crash_ts,
    crashes.day_night,
    crashes.stats_area,
    crashes.suburb,
    crashes.postcode,
    crashes.lga_name,
    crashes.lga_missing,
    crashes.crash_type,
    crashes.severity_code,
    severity.severity_name,
    severity.is_fsi,
    severity.is_casualty_crash,
    crashes.total_units,
    crashes.total_cas,
    crashes.total_fats,
    crashes.total_si,
    crashes.total_mi,
    coalesce(casualty_counts.casualty_rows, 0) as casualty_rows,
    coalesce(casualty_counts.fatal_casualties, 0) as fatal_casualties,
    coalesce(casualty_counts.admitted_casualties, 0) as admitted_casualties,
    coalesce(casualty_counts.minor_casualties, 0) as minor_casualties,
    crashes.speed_limit_kmh,
    crashes.position_type,
    crashes.road_surface,
    crashes.moisture_cond,
    crashes.weather_cond,
    crashes.traffic_controls,
    crashes.entity_responsible,
    crashes.dui_involved,
    crashes.drugs_involved,
    crashes.accloc_x_epsg8059,
    crashes.accloc_y_epsg8059,
    regimes.regime_id as pdo_regime_id,
    crashes.crash_year = latest.provisional_year as is_provisional,
    crashes.release_id,
    crashes.release_as_at
from crashes
inner join severity on crashes.severity_code = severity.severity_code
left join casualty_counts on crashes.crash_id = casualty_counts.crash_id
left join regimes
    on crashes.crash_month between regimes.valid_from and coalesce(regimes.valid_to, date '9999-12-31')
cross join latest
order by crashes.crash_month, crashes.lga_name, crashes.severity_code, crashes.crash_id
