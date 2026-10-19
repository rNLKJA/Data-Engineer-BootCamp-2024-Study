-- One-row headline numbers for the dashboard KPI strip.
with crashes as (
    select
        min(crash_year) as first_year,
        max(crash_year) as last_year,
        count(*) as crashes,
        count(*) filter (where is_casualty_crash) as casualty_crashes,
        count(*) filter (where is_fsi) as fsi_crashes,
        count(*) filter (where severity_code = 4) as fatal_crashes,
        sum(total_cas) as casualties,
        sum(total_fats) as fatalities,
        sum(total_si) as serious_injuries,
        count(distinct crash_month) as months_with_crashes,
        -- Councils only: excludes the unincorporated groupings and missing LGAs.
        count(distinct lga_name) filter (where lga_name not like '%UNINCORP%') as council_areas,
        count(*) filter (where lga_missing) as crashes_without_lga,
        count(distinct release_id) as releases
    from {{ ref('fct_crashes') }}
),

months as (
    select count(*) as months from {{ ref('rpt_monthly_severity') }}
)

select crashes.*, months.months
from crashes
cross join months
