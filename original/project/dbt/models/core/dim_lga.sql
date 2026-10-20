-- One row per local government area (council). Some councils straddle the
-- Metropolitan and Country statistical areas, so main_stats_area is the area
-- holding most of the council's crashes (ties broken alphabetically).
with by_area as (
    select lga_name, stats_area, count(*) as crashes
    from {{ ref('fct_crashes') }}
    group by lga_name, stats_area
),

ranked as (
    select
        *,
        row_number() over (partition by lga_name order by crashes desc, stats_area) as area_rank,
        count(*) over (partition by lga_name) as stats_areas,
        sum(crashes) over (partition by lga_name) as total_crashes
    from by_area
)

select
    lga_name,
    stats_area as main_stats_area,
    stats_areas,
    total_crashes as crashes,
    lga_name = 'UNINCORPORATED OR UNKNOWN' as is_unknown
from ranked
where area_rank = 1
order by lga_name
