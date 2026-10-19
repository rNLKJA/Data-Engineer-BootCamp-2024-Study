-- Optional tile 3: people killed (within 30 days) and people admitted to
-- hospital per year, counted from casualty rows, next to the crash totals.
with people as (
    select
        crash_year,
        count(*) as casualties,
        count(*) filter (where is_fatality) as fatalities,
        count(*) filter (where is_admitted) as admitted_to_hospital
    from {{ ref('fct_casualties') }}
    group by crash_year
),

crashes as (
    select
        crash_year,
        count(*) as crashes,
        count(*) filter (where severity_code = 4) as fatal_crashes,
        count(*) filter (where severity_code = 3) as serious_injury_crashes,
        count(*) filter (where is_fsi) as fsi_crashes,
        sum(total_fats) as total_fats,
        sum(total_si) as total_si,
        bool_or(is_provisional) as is_provisional
    from {{ ref('fct_crashes') }}
    group by crash_year
)

select
    crashes.crash_year,
    crashes.crashes,
    crashes.fatal_crashes,
    crashes.serious_injury_crashes,
    crashes.fsi_crashes,
    coalesce(people.casualties, 0) as casualties,
    coalesce(people.fatalities, 0) as fatalities,
    coalesce(people.admitted_to_hospital, 0) as admitted_to_hospital,
    crashes.total_fats,
    crashes.total_si,
    crashes.is_provisional
from crashes
left join people on crashes.crash_year = people.crash_year
order by crashes.crash_year
