-- Every crash has exactly as many casualty rows as its Total Cas.
select crash_id, total_cas, casualty_rows
from {{ ref('fct_crashes') }}
where casualty_rows <> total_cas
