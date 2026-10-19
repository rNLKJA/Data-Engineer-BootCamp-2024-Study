-- One row per casualty. AGE uses "XXX" for unknown, which becomes NULL.
with source as (
    select * from {{ source('lake', 'casualty') }}
)

select
    "REPORT_ID" as crash_id,
    "UND_UNIT_NUMBER" as unit_number,
    "CASUALTY_NUMBER" as casualty_number,
    "Casualty Type" as casualty_type,
    "Sex" as sex,
    try_cast("AGE" as integer) as age,
    "Position In Veh" as position_in_vehicle,
    "Thrown Out" as thrown_out,
    -- Fatal / Admitted to Hospital / Treated at Hospital / By Private
    "Injury Extent" as injury_extent,
    "Seat Belt" as seat_belt,
    "Helmet" as helmet,
    "Hospital" as hospital,
    cast(year as integer) as crash_year,
    _release_id as release_id,
    _as_at as release_as_at
from source
