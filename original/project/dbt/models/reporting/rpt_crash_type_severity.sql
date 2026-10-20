-- Tile 1: severity mix per DIT crash type, ranked by FSI crashes.
with by_type as (
    select
        crash_type,
        count(*) as crashes,
        count(*) filter (where severity_code = 1) as pdo_crashes,
        count(*) filter (where severity_code = 2) as minor_injury_crashes,
        count(*) filter (where severity_code = 3) as serious_injury_crashes,
        count(*) filter (where severity_code = 4) as fatal_crashes,
        count(*) filter (where is_fsi) as fsi_crashes,
        count(*) filter (where is_casualty_crash) as casualty_crashes,
        sum(total_fats) as fatalities,
        sum(total_si) as serious_injuries
    from {{ ref('fct_crashes') }}
    group by crash_type
)

select
    *,
    round(100.0 * fsi_crashes / nullif(casualty_crashes, 0), 2) as fsi_pct_of_casualty_crashes,
    round(100.0 * fatal_crashes / nullif(fsi_crashes, 0), 2) as fatal_pct_of_fsi,
    round(100.0 * fsi_crashes / sum(fsi_crashes) over (), 2) as pct_of_all_fsi,
    row_number() over (order by fsi_crashes desc, crash_type) as fsi_rank
from by_type
order by fsi_rank
