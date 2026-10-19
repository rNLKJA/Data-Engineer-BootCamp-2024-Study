-- One row per casualty with the crash attributes needed for reporting.
select
    casualties.crash_id,
    casualties.unit_number,
    casualties.casualty_number,
    casualties.casualty_type,
    casualties.sex,
    casualties.age,
    casualties.position_in_vehicle,
    casualties.thrown_out,
    casualties.injury_extent,
    casualties.injury_extent = 'Fatal' as is_fatality,
    casualties.injury_extent = 'Admitted to Hospital' as is_admitted,
    casualties.seat_belt,
    casualties.helmet,
    crashes.crash_year,
    crashes.crash_month,
    crashes.lga_name,
    crashes.stats_area,
    crashes.crash_type,
    crashes.severity_code,
    crashes.is_provisional
from {{ ref('stg_casualties') }} as casualties
inner join {{ ref('fct_crashes') }} as crashes on casualties.crash_id = crashes.crash_id
order by crashes.crash_month, casualties.crash_id, casualties.unit_number, casualties.casualty_number
