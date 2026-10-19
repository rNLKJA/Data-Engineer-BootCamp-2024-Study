-- After alias mapping, every council named in the 2012-2020 releases also
-- appears in the 2021-2025 release. A failure means DIT changed a spelling and
-- seeds/lga_name_aliases.csv needs a new row. Unincorporated groupings are
-- excluded because they are sparse. Tagged full_data: it only makes sense on
-- the complete release set, not on the small test fixture.
{{ config(tags=['full_data']) }}

with names as (
    select lga_name, min(crash_year) as first_year, max(crash_year) as last_year
    from {{ ref('stg_crashes') }}
    where lga_name not like '%UNINCORP%'
    group by lga_name
),

latest_release as (
    select min(first_year) as first_year
    from {{ source('lake', 'releases') }}
    where as_at = (select max(as_at) from {{ source('lake', 'releases') }})
)

select names.lga_name, names.first_year, names.last_year
from names, latest_release
where names.last_year < latest_release.first_year
