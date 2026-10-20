-- Casualty rows with Injury Extent = Fatal equal Total Fats for every crash.
select crash_id, total_fats, fatal_casualties
from {{ ref('fct_crashes') }}
where fatal_casualties <> total_fats
