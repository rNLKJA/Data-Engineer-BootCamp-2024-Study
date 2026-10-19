-- Casualty rows per crash by injury extent, used to reconcile with the crash totals.
select
    crash_id,
    count(*) as casualty_rows,
    count(*) filter (where injury_extent = 'Fatal') as fatal_casualties,
    count(*) filter (where injury_extent = 'Admitted to Hospital') as admitted_casualties,
    count(*) filter (where injury_extent in ('Treated at Hospital', 'By Private')) as minor_casualties
from {{ ref('stg_casualties') }}
group by crash_id
