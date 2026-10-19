-- Tile 2: one row per calendar month across every release year, including
-- months with no crashes, with FSI (fatal + serious injury) counts and a
-- trailing 12-month mean. All-crash counts are kept for context only: PDO
-- reporting rules changed in 2013, December 2016 and 2017.
with bounds as (
    select
        make_date(min(first_year), 1, 1) as first_month,
        make_date(max(last_year), 12, 1) as last_month
    from {{ source('lake', 'releases') }}
),

spine as (
    select cast(generate_series as date) as crash_month
    from bounds, generate_series(bounds.first_month, bounds.last_month, interval 1 month)
),

counts as (
    select
        crash_month,
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
    group by crash_month
),

regimes as (
    select * from {{ ref('pdo_reporting_regimes') }}
),

monthly as (
    select
        spine.crash_month,
        coalesce(counts.crashes, 0) as crashes,
        coalesce(counts.pdo_crashes, 0) as pdo_crashes,
        coalesce(counts.minor_injury_crashes, 0) as minor_injury_crashes,
        coalesce(counts.serious_injury_crashes, 0) as serious_injury_crashes,
        coalesce(counts.fatal_crashes, 0) as fatal_crashes,
        coalesce(counts.fsi_crashes, 0) as fsi_crashes,
        coalesce(counts.casualty_crashes, 0) as casualty_crashes,
        coalesce(counts.fatalities, 0) as fatalities,
        coalesce(counts.serious_injuries, 0) as serious_injuries
    from spine
    left join counts on spine.crash_month = counts.crash_month
)

select
    monthly.crash_month,
    year(monthly.crash_month) as crash_year,
    month(monthly.crash_month) as month_number,
    monthly.crashes,
    monthly.pdo_crashes,
    monthly.minor_injury_crashes,
    monthly.serious_injury_crashes,
    monthly.fatal_crashes,
    monthly.fsi_crashes,
    monthly.casualty_crashes,
    monthly.fatalities,
    monthly.serious_injuries,
    case
        when count(*) over trailing_year = 12 then avg(monthly.fsi_crashes) over trailing_year
    end as fsi_rolling_12_mean,
    regimes.regime_id as pdo_regime_id,
    year(monthly.crash_month) = (select max(last_year) from {{ source('lake', 'releases') }}) as is_provisional
from monthly
left join regimes
    on monthly.crash_month between regimes.valid_from and coalesce(regimes.valid_to, date '9999-12-31')
window trailing_year as (order by monthly.crash_month rows between 11 preceding and current row)
order by monthly.crash_month
