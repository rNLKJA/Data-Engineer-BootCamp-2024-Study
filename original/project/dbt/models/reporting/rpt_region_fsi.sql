-- Supporting question: FSI crashes by DIT statistical area (City, Metropolitan, Country).
select
    stats_area,
    count(*) as crashes,
    count(*) filter (where is_casualty_crash) as casualty_crashes,
    count(*) filter (where is_fsi) as fsi_crashes,
    count(*) filter (where severity_code = 4) as fatal_crashes,
    count(*) filter (where severity_code = 3) as serious_injury_crashes,
    sum(total_fats) as fatalities,
    round(100.0 * count(*) filter (where is_fsi) / nullif(count(*) filter (where is_casualty_crash), 0), 2)
        as fsi_pct_of_casualty_crashes,
    round(100.0 * count(*) filter (where is_fsi) / sum(count(*) filter (where is_fsi)) over (), 2) as pct_of_all_fsi
from {{ ref('fct_crashes') }}
group by stats_area
order by fsi_crashes desc, stats_area
