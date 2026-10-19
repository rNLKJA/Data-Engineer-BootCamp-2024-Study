# Test fixtures

A small slice of the real DIT road crash data, used by the offline tests so they
run without a network connection.

- `2019_DATA_SA_*.csv`: 100 crashes from `2019_data_sa_as_at_20210527.zip`
  (40 property damage only, 30 minor injury, 20 serious injury, 10 fatal), with
  all 73 casualty rows and 208 unit rows that belong to them.
- `2021-2025_DATA_SA_*.csv`: 100 crashes from 2023 in
  `2021-2025_data_sa_crash_as_at_20261009.zip` (same severity mix), with all 75
  casualty rows and 211 unit rows that belong to them.

Rows were chosen deterministically (ordered by the MD5 of `REPORT_ID`) by
`scripts/make_fixtures.py`, and source lines are copied byte for byte, so the
quoting and CRLF line endings match what DIT publishes. The tests zip these
files on the fly and compute the checksums they pin.

Attribution: Road Crash Data, Department for Infrastructure and Transport
(Government of South Australia), data.sa.gov.au, CC BY 4.0
(http://creativecommons.org/licenses/by/4.0). The rows are unchanged apart from
the selection.
