-- One row per unit involved in a crash. "X", "XXX" and "XXXX" mean unknown.
with source as (
    select * from {{ source('lake', 'units') }}
)

select
    "REPORT_ID" as crash_id,
    "Unit No" as unit_number,
    "No Of Cas" as casualties_in_unit,
    "Veh Reg State" as veh_reg_state,
    "Unit Type" as unit_type,
    try_cast("Veh Year" as integer) as vehicle_year,
    "Direction Of Travel" as direction_of_travel,
    "Sex" as controller_sex,
    try_cast("Age" as integer) as controller_age,
    "Lic State" as licence_state,
    "Licence Class" as licence_class,
    "Licence Type" as licence_type,
    "Towing" as towing,
    "Unit Movement" as unit_movement,
    try_cast("Number Occupants" as integer) as number_occupants,
    -- Residential postcode of the unit, not the crash location.
    "Postcode" as unit_postcode,
    coalesce("Rollover" = 'Y', false) as rollover,
    coalesce("Fire" = 'Y', false) as fire,
    cast(year as integer) as crash_year,
    _release_id as release_id
from source
