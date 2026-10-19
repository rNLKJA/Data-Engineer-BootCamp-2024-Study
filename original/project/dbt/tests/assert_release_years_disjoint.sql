-- Release year ranges never overlap, and each crash year in the lake comes
-- from exactly one release.
with releases as (
    select * from {{ source('lake', 'releases') }}
),

overlapping_releases as (
    select a.release_id || ' overlaps ' || b.release_id as problem
    from releases as a
    inner join releases as b
        on a.release_id < b.release_id
        and a.first_year <= b.last_year
        and b.first_year <= a.last_year
),

years_with_many_releases as (
    select 'year ' || crash_year || ' loaded from ' || count(distinct release_id) || ' releases' as problem
    from {{ ref('stg_crashes') }}
    group by crash_year
    having count(distinct release_id) > 1
)

select problem from overlapping_releases
union all
select problem from years_with_many_releases
