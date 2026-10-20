-- Every crash month falls inside the year range of the release it came from.
select crashes.crash_id, crashes.crash_month, crashes.release_id, releases.first_year, releases.last_year
from {{ ref('stg_crashes') }} as crashes
left join {{ source('lake', 'releases') }} as releases on crashes.release_id = releases.release_id
where releases.release_id is null
    or crashes.crash_month < make_date(releases.first_year, 1, 1)
    or crashes.crash_month > make_date(releases.last_year, 12, 1)
