-- One row per local government area (council) name in the data. Some councils
-- straddle the Metropolitan and Country statistical areas, so main_stats_area is
-- the area holding most of the council's crashes (ties broken alphabetically).
-- Four names are not councils: UNINCORPORATED OR UNKNOWN (no LGA recorded) and
-- DIT's three unincorporated-area groupings. is_council excludes all of them.
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
    lga_name = 'UNINCORPORATED OR UNKNOWN' as is_unknown,
    lga_name not like '%UNINCORP%' as is_council
from ranked
where area_rank = 1
order by lga_name
