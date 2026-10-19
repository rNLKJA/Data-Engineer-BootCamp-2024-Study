-- Every crash has exactly as many unit rows as its Total Units.
with unit_rows as (
    select crash_id, count(*) as unit_rows
    from {{ ref('stg_units') }}
    group by crash_id
)

select crashes.crash_id, crashes.total_units, coalesce(unit_rows.unit_rows, 0) as unit_rows
from {{ ref('stg_crashes') }} as crashes
left join unit_rows on crashes.crash_id = unit_rows.crash_id
where coalesce(unit_rows.unit_rows, 0) <> crashes.total_units
