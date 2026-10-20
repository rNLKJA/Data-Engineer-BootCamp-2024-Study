-- Supporting question: FSI crashes per council area across all years.
-- Counts are not rates: there is no population or traffic exposure here.
-- Only councils are ranked. Crashes with no council recorded and DIT's
-- unincorporated-area groupings keep their rows, with a NULL fsi_rank, so the
-- dashboard can show them separately instead of ranking them as councils.
with by_lga as (
    select
        crashes.lga_name,
        lga.main_stats_area,
        lga.stats_areas,
        lga.is_unknown,
        lga.is_council,
        count(*) as crashes,
        count(*) filter (where crashes.is_fsi) as fsi_crashes,
        count(*) filter (where crashes.severity_code = 4) as fatal_crashes,
        count(*) filter (where crashes.severity_code = 3) as serious_injury_crashes,
        sum(crashes.total_fats) as fatalities,
        round(100.0 * count(*) filter (where crashes.is_fsi) / nullif(count(*) filter (where crashes.is_casualty_crash), 0), 2)
            as fsi_pct_of_casualty_crashes
    from {{ ref('fct_crashes') }} as crashes
    inner join {{ ref('dim_lga') }} as lga on crashes.lga_name = lga.lga_name
    group by crashes.lga_name, lga.main_stats_area, lga.stats_areas, lga.is_unknown, lga.is_council
)

select
    *,
    case
        when is_council then row_number() over (partition by is_council order by fsi_crashes desc, lga_name)
    end as fsi_rank
from by_lga
order by is_council desc, fsi_rank, fsi_crashes desc, lga_name
