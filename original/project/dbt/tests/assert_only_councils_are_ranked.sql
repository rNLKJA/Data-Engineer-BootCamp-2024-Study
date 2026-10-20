-- The council ranking on the dashboard must not rank a non-council: crashes
-- with no LGA recorded (UNINCORPORATED OR UNKNOWN) and DIT's unincorporated-area
-- groupings have no fsi_rank, and every council has one.
select lga_name, is_council, fsi_rank
from {{ ref('rpt_lga_fsi') }}
where (fsi_rank is null) = is_council
