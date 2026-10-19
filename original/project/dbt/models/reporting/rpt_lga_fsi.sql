-- Supporting question: FSI crashes per council area across all years.
-- Counts are not rates: there is no population or traffic exposure here.
select
    crashes.lga_name,
    lga.main_stats_area,
    lga.is_unknown,
    count(*) as crashes,
    count(*) filter (where crashes.is_fsi) as fsi_crashes,
    count(*) filter (where crashes.severity_code = 4) as fatal_crashes,
    count(*) filter (where crashes.severity_code = 3) as serious_injury_crashes,
    sum(crashes.total_fats) as fatalities,
    round(100.0 * count(*) filter (where crashes.is_fsi) / nullif(count(*) filter (where crashes.is_casualty_crash), 0), 2)
        as fsi_pct_of_casualty_crashes,
    row_number() over (order by count(*) filter (where crashes.is_fsi) desc, crashes.lga_name) as fsi_rank
from {{ ref('fct_crashes') }} as crashes
inner join {{ ref('dim_lga') }} as lga on crashes.lga_name = lga.lga_name
group by crashes.lga_name, lga.main_stats_area, lga.is_unknown
order by fsi_rank
