-- One row per crash, with snake_case names and parsed types.
with source as (
    select * from {{ source('lake', 'crash') }}
),

aliases as (
    -- The 2012-2020 extracts spell 33 council names differently from the
    -- 2021-2025 extract ("CC MARION." vs "CC MARION"); map them to the newer form.
    select * from {{ ref('lga_name_aliases') }}
)

select
    "REPORT_ID" as crash_id,
    cast(year as integer) as crash_year,
    month(strptime("Month", '%B')) as crash_month_number,
    make_date(cast(year as integer), month(strptime("Month", '%B')), 1) as crash_month,
    "Day" as day_of_week,
    "Time" as crash_time_text,
    -- Time is a 12-hour clock string such as "08:30 am".
    hour(strptime("Time", '%I:%M %p')) as crash_hour,
    -- Full timestamp only exists in extracts from 2021 ("18/1/2022 13:50:00").
    try_strptime("Crash Date Time", '%d/%m/%Y %H:%M:%S') as crash_ts,
    "DayNight" as day_night,
    -- "1 City", "2 Metropolitan", "3 Country" -> City, Metropolitan, Country
    regexp_replace("Stats Area", '^[0-9]+\s+', '') as stats_area,
    "Suburb" as suburb,
    "Postcode" as postcode,
    -- Crashes with no LGA recorded are grouped as UNINCORPORATED OR UNKNOWN.
    coalesce(aliases.lga_name, nullif(trim("LGA Name"), ''), 'UNINCORPORATED OR UNKNOWN') as lga_name,
    "LGA Name" as lga_name_raw,
    "LGA Name" is null or trim("LGA Name") = '' as lga_missing,
    "Total Units" as total_units,
    "Total Cas" as total_cas,
    "Total Fats" as total_fats,
    "Total SI" as total_si,
    "Total MI" as total_mi,
    -- Speed zone arrives zero padded ("060").
    try_cast("Area Speed" as integer) as speed_limit_kmh,
    "Position Type" as position_type,
    "Horizontal Align" as horizontal_align,
    "Vertical Align" as vertical_align,
    "Other Feat" as other_feature,
    "Road Surface" as road_surface,
    "Moisture Cond" as moisture_cond,
    "Weather Cond" as weather_cond,
    "Crash Type" as crash_type,
    "Unit Resp" as unit_responsible,
    "Entity Code" as entity_responsible,
    "CSEF Severity" as csef_severity,
    cast(split_part("CSEF Severity", ':', 1) as integer) as severity_code,
    "Traffic Ctrls" as traffic_controls,
    coalesce("DUI Involved" = 'Y', false) as dui_involved,
    coalesce("Drugs Involved" = 'Y', false) as drugs_involved,
    -- Lambert conformal conic, GDA2020 (EPSG:8059), metres.
    "ACCLOC_X" as accloc_x_epsg8059,
    "ACCLOC_Y" as accloc_y_epsg8059,
    "UNIQUE_LOC" as unique_loc,
    _release_id as release_id,
    _as_at as release_as_at,
    _ingested_from as ingested_from
from source
left join aliases on trim(source."LGA Name") = aliases.raw_lga_name
