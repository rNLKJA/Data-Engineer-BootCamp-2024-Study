# Run log

Real terminal output of `scripts/run_all.sh` (which runs `make all`) on the machine
and date shown below. Nothing here is edited except that this header was added.
Prefect log times are in the machine's local time (ACDT, UTC+1030); dbt log times are in UTC.

```text
$ date -u
Tue Oct 20 00:31:50 UTC 2026
$ uname -sm
Darwin arm64
$ .venv/bin/python --version
Python 3.11.14
$ rm -rf data/landing data/lake data/warehouse dbt/target
$ ls -l data/landing
(empty: first run downloads every release)
$ make all
.venv/bin/python -m pipeline.flow
11:01:52.523 | INFO    | prefect - Starting temporary server on http://127.0.0.1:8078
See https://docs.prefect.io/v3/concepts/server#how-to-guides for more information on running a dedicated Prefect server.
11:01:53.919 | INFO    | Flow run 'visionary-dolphin' - Beginning flow run 'visionary-dolphin' for flow 'sa_crash_pipeline'
11:01:53.923 | INFO    | Flow run 'visionary-dolphin' - manifest: 10 releases covering 2012-2025 (14 years)
11:02:54.063 | WARNING | pipeline.ingest - sa_crash_2012_as_at_20210527: attempt 1/3 failed (ReadTimeout: HTTPSConnectionPool(host='data.sa.gov.au', port=443): Read timed out. (read timeout=60.0)), retrying in 2.0s
11:03:06.215 | WARNING | pipeline.ingest - sa_crash_2012_as_at_20210527: attempt 2/3 failed (HTTP 504), retrying in 4.0s
11:03:20.422 | INFO    | Task run 'fetch_release-41c' - Task run failed with exception: SourceUnavailableError('sa_crash_2012_as_at_20210527: gave up after 3 attempts (HTTP 504) for https://data.sa.gov.au/data/dataset/21386a53-56a1-4edf-bd0b-61ed15f10acf/resource/922cd06b-76e4-40bf-a534-ce2f2daae904/download/2012_data_sa_as_at_20210527.zip') - Retry 1/2 will start 10 second(s) from now
11:04:30.529 | WARNING | pipeline.ingest - sa_crash_2012_as_at_20210527: attempt 1/3 failed (ReadTimeout: HTTPSConnectionPool(host='data.sa.gov.au', port=443): Read timed out. (read timeout=60.0)), retrying in 2.0s
11:05:15.978 | INFO    | Task run 'fetch_release-41c' - sa_crash_2012_as_at_20210527: downloaded 2012_data_sa_as_at_20210527.zip (1628505 bytes, sha256 02380fee078e...)
11:05:15.982 | INFO    | Task run 'fetch_release-41c' - Finished in state Completed()
11:05:16.156 | INFO    | Task run 'validate_schema-25f' - sa_crash_2012_as_at_20210527: header contract ok; rows crash=22829 casualty=7479 units=48320
11:05:16.157 | INFO    | Task run 'validate_schema-25f' - Finished in state Completed()
11:05:16.417 | INFO    | Task run 'load_to_lake-d50' - sa_crash_2012_as_at_20210527: wrote years 2012-2012 to lake; crash=22829 casualty=7479 units=48320
11:05:16.417 | INFO    | Task run 'load_to_lake-d50' - Finished in state Completed()
11:05:18.597 | INFO    | Task run 'fetch_release-91d' - sa_crash_2013_as_at_20210527: downloaded 2013_data_sa_as_at_20210527.zip (1257991 bytes, sha256 697e5ae5b0dd...)
11:05:18.599 | INFO    | Task run 'fetch_release-91d' - Finished in state Completed()
11:05:18.730 | INFO    | Task run 'validate_schema-409' - sa_crash_2013_as_at_20210527: header contract ok; rows crash=16675 casualty=7177 units=35865
11:05:18.731 | INFO    | Task run 'validate_schema-409' - Finished in state Completed()
11:05:18.946 | INFO    | Task run 'load_to_lake-393' - sa_crash_2013_as_at_20210527: wrote years 2013-2013 to lake; crash=16675 casualty=7177 units=35865
11:05:18.947 | INFO    | Task run 'load_to_lake-393' - Finished in state Completed()
11:05:20.352 | INFO    | Task run 'fetch_release-6eb' - sa_crash_2014_as_at_20210527: downloaded 2014_data_sa_as_at_20210527.zip (1221928 bytes, sha256 d6ff9170c6ef...)
11:05:20.355 | INFO    | Task run 'fetch_release-6eb' - Finished in state Completed()
11:05:20.501 | INFO    | Task run 'validate_schema-9d9' - sa_crash_2014_as_at_20210527: header contract ok; rows crash=16162 casualty=6982 units=34552
11:05:20.502 | INFO    | Task run 'validate_schema-9d9' - Finished in state Completed()
11:05:20.707 | INFO    | Task run 'load_to_lake-605' - sa_crash_2014_as_at_20210527: wrote years 2014-2014 to lake; crash=16162 casualty=6982 units=34552
11:05:20.708 | INFO    | Task run 'load_to_lake-605' - Finished in state Completed()
11:05:22.102 | INFO    | Task run 'fetch_release-622' - sa_crash_2015_as_at_20210527: downloaded 2015_data_sa_as_at_20210527.zip (1168394 bytes, sha256 8aa9d4b9bca0...)
11:05:22.105 | INFO    | Task run 'fetch_release-622' - Finished in state Completed()
11:05:22.250 | INFO    | Task run 'validate_schema-6e6' - sa_crash_2015_as_at_20210527: header contract ok; rows crash=15431 casualty=6660 units=33084
11:05:22.251 | INFO    | Task run 'validate_schema-6e6' - Finished in state Completed()
11:05:22.453 | INFO    | Task run 'load_to_lake-967' - sa_crash_2015_as_at_20210527: wrote years 2015-2015 to lake; crash=15431 casualty=6660 units=33084
11:05:22.454 | INFO    | Task run 'load_to_lake-967' - Finished in state Completed()
11:05:24.534 | INFO    | Task run 'fetch_release-739' - sa_crash_2016_as_at_20210527: downloaded 2016_data_sa_as_at_20210527.zip (1259179 bytes, sha256 3d1ce02ebe9d...)
11:05:24.538 | INFO    | Task run 'fetch_release-739' - Finished in state Completed()
11:05:24.685 | INFO    | Task run 'validate_schema-2a0' - sa_crash_2016_as_at_20210527: header contract ok; rows crash=16775 casualty=6565 units=35861
11:05:24.686 | INFO    | Task run 'validate_schema-2a0' - Finished in state Completed()
11:05:24.897 | INFO    | Task run 'load_to_lake-f3e' - sa_crash_2016_as_at_20210527: wrote years 2016-2016 to lake; crash=16775 casualty=6565 units=35861
11:05:24.898 | INFO    | Task run 'load_to_lake-f3e' - Finished in state Completed()
11:05:26.079 | INFO    | Task run 'fetch_release-63e' - sa_crash_2017_as_at_20210527: downloaded 2017_data_sa_as_at_20210527.zip (1001803 bytes, sha256 a97b3c4e877c...)
11:05:26.081 | INFO    | Task run 'fetch_release-63e' - Finished in state Completed()
11:05:26.217 | INFO    | Task run 'validate_schema-456' - sa_crash_2017_as_at_20210527: header contract ok; rows crash=13236 casualty=6237 units=28161
11:05:26.218 | INFO    | Task run 'validate_schema-456' - Finished in state Completed()
11:05:26.394 | INFO    | Task run 'load_to_lake-806' - sa_crash_2017_as_at_20210527: wrote years 2017-2017 to lake; crash=13236 casualty=6237 units=28161
11:05:26.395 | INFO    | Task run 'load_to_lake-806' - Finished in state Completed()
11:05:27.632 | INFO    | Task run 'fetch_release-614' - sa_crash_2018_as_at_20210527: downloaded 2018_data_sa_as_at_20210527.zip (1024690 bytes, sha256 c7fad62e2f7b...)
11:05:27.634 | INFO    | Task run 'fetch_release-614' - Finished in state Completed()
11:05:27.767 | INFO    | Task run 'validate_schema-e81' - sa_crash_2018_as_at_20210527: header contract ok; rows crash=13599 casualty=6124 units=29033
11:05:27.768 | INFO    | Task run 'validate_schema-e81' - Finished in state Completed()
11:05:27.946 | INFO    | Task run 'load_to_lake-850' - sa_crash_2018_as_at_20210527: wrote years 2018-2018 to lake; crash=13599 casualty=6124 units=29033
11:05:27.947 | INFO    | Task run 'load_to_lake-850' - Finished in state Completed()
11:05:29.158 | INFO    | Task run 'fetch_release-e73' - sa_crash_2019_as_at_20210527: downloaded 2019_data_sa_as_at_20210527.zip (980081 bytes, sha256 aef9a66aef27...)
11:05:29.161 | INFO    | Task run 'fetch_release-e73' - Finished in state Completed()
11:05:29.274 | INFO    | Task run 'validate_schema-7fb' - sa_crash_2019_as_at_20210527: header contract ok; rows crash=12964 casualty=6031 units=27714
11:05:29.275 | INFO    | Task run 'validate_schema-7fb' - Finished in state Completed()
11:05:29.453 | INFO    | Task run 'load_to_lake-d0f' - sa_crash_2019_as_at_20210527: wrote years 2019-2019 to lake; crash=12964 casualty=6031 units=27714
11:05:29.454 | INFO    | Task run 'load_to_lake-d0f' - Finished in state Completed()
11:05:31.241 | INFO    | Task run 'fetch_release-54d' - sa_crash_2020_as_at_20210527: downloaded 2020_data_sa_as_at_20210527.zip (865285 bytes, sha256 8a5f4269d900...)
11:05:31.244 | INFO    | Task run 'fetch_release-54d' - Finished in state Completed()
11:05:31.367 | INFO    | Task run 'validate_schema-da6' - sa_crash_2020_as_at_20210527: header contract ok; rows crash=11534 casualty=4877 units=24539
11:05:31.368 | INFO    | Task run 'validate_schema-da6' - Finished in state Completed()
11:05:31.525 | INFO    | Task run 'load_to_lake-f90' - sa_crash_2020_as_at_20210527: wrote years 2020-2020 to lake; crash=11534 casualty=4877 units=24539
11:05:31.526 | INFO    | Task run 'load_to_lake-f90' - Finished in state Completed()
11:05:33.992 | INFO    | Task run 'fetch_release-3dc' - sa_crash_2021_2025_as_at_20261009: downloaded 2021-2025_data_sa_crash_as_at_20261009.zip (5155745 bytes, sha256 2c6df4a4bcae...)
11:05:33.996 | INFO    | Task run 'fetch_release-3dc' - Finished in state Completed()
11:05:34.206 | INFO    | Task run 'validate_schema-fe1' - sa_crash_2021_2025_as_at_20261009: header contract ok; rows crash=65655 casualty=23751 units=140150
11:05:34.207 | INFO    | Task run 'validate_schema-fe1' - Finished in state Completed()
11:05:34.610 | INFO    | Task run 'load_to_lake-d7d' - sa_crash_2021_2025_as_at_20261009: wrote years 2021-2025 to lake; crash=65655 casualty=23751 units=140150
11:05:34.611 | INFO    | Task run 'load_to_lake-d7d' - Finished in state Completed()
11:05:34.627 | INFO    | Flow run 'visionary-dolphin' - lake has 14 crash year partitions (2012-2025); removed 0 stale
00:35:34  Running with dbt=1.12.6
00:35:34  Registered adapter: duckdb=1.11.0
00:35:34  Unable to do partial parsing because saved manifest not found. Starting full parse.
00:35:35  Found 13 models, 64 data tests, 3 seeds, 4 sources, 501 macros
00:35:35  
00:35:35  Concurrency: 4 threads (target='dev')
00:35:35  
00:35:35  1 of 80 START sql view model main.stg_casualties ............................... [RUN]
00:35:35  2 of 80 START sql view model main.stg_units .................................... [RUN]
00:35:35  3 of 80 START seed file main.lga_name_aliases .................................. [RUN]
00:35:35  4 of 80 START seed file main.pdo_reporting_regimes ............................. [RUN]
00:35:35  4 of 80 OK loaded seed file main.pdo_reporting_regimes ......................... [INSERT 4 in 0.05s]
00:35:35  3 of 80 OK loaded seed file main.lga_name_aliases .............................. [INSERT 33 in 0.05s]
00:35:35  5 of 80 START seed file main.severity_levels ................................... [RUN]
00:35:35  6 of 80 START test not_null_pdo_reporting_regimes_regime_id .................... [RUN]
00:35:35  2 of 80 OK created sql view model main.stg_units ............................... [OK in 0.05s]
00:35:35  1 of 80 OK created sql view model main.stg_casualties .......................... [OK in 0.05s]
00:35:35  7 of 80 START test unique_pdo_reporting_regimes_regime_id ...................... [RUN]
00:35:35  8 of 80 START test not_null_lga_name_aliases_raw_lga_name ...................... [RUN]
00:35:35  6 of 80 PASS not_null_pdo_reporting_regimes_regime_id .......................... [PASS in 0.03s]
00:35:35  7 of 80 PASS unique_pdo_reporting_regimes_regime_id ............................ [PASS in 0.02s]
00:35:35  8 of 80 PASS not_null_lga_name_aliases_raw_lga_name ............................ [PASS in 0.02s]
00:35:35  9 of 80 START test unique_lga_name_aliases_raw_lga_name ........................ [RUN]
00:35:35  5 of 80 OK loaded seed file main.severity_levels ............................... [INSERT 4 in 0.03s]
00:35:35  10 of 80 START test non_negative_stg_units_casualties_in_unit .................. [RUN]
00:35:35  11 of 80 START test not_null_stg_units_crash_id ................................ [RUN]
00:35:35  12 of 80 START test accepted_values_stg_casualties_injury_extent__Fatal__Admitted_to_Hospital__Treated_at_Hospital__By_Private  [RUN]
00:35:35  9 of 80 PASS unique_lga_name_aliases_raw_lga_name .............................. [PASS in 0.02s]
00:35:35  10 of 80 PASS non_negative_stg_units_casualties_in_unit ........................ [PASS in 0.02s]
00:35:35  13 of 80 START test non_negative_stg_casualties_age ............................ [RUN]
00:35:35  12 of 80 PASS accepted_values_stg_casualties_injury_extent__Fatal__Admitted_to_Hospital__Treated_at_Hospital__By_Private  [PASS in 0.02s]
00:35:35  11 of 80 PASS not_null_stg_units_crash_id ...................................... [PASS in 0.02s]
00:35:35  14 of 80 START test not_null_stg_casualties_crash_id ........................... [RUN]
00:35:35  15 of 80 START test not_null_severity_levels_severity_code ..................... [RUN]
00:35:35  16 of 80 START test unique_severity_levels_severity_code ....................... [RUN]
00:35:35  13 of 80 PASS non_negative_stg_casualties_age .................................. [PASS in 0.02s]
00:35:35  15 of 80 PASS not_null_severity_levels_severity_code ........................... [PASS in 0.02s]
00:35:35  16 of 80 PASS unique_severity_levels_severity_code ............................. [PASS in 0.02s]
00:35:35  17 of 80 START sql view model main.stg_crashes ................................. [RUN]
00:35:35  14 of 80 PASS not_null_stg_casualties_crash_id ................................. [PASS in 0.02s]
00:35:35  18 of 80 START sql view model main.int_casualty_counts ......................... [RUN]
00:35:36  18 of 80 OK created sql view model main.int_casualty_counts .................... [OK in 0.01s]
00:35:36  17 of 80 OK created sql view model main.stg_crashes ............................ [OK in 0.01s]
00:35:36  19 of 80 START test accepted_values_stg_crashes_severity_code__False__1__2__3__4  [RUN]
00:35:36  20 of 80 START test accepted_values_stg_crashes_stats_area__City__Metropolitan__Country  [RUN]
00:35:36  21 of 80 START test assert_lga_names_stable_across_releases .................... [RUN]
00:35:36  22 of 80 START test assert_month_within_release ................................ [RUN]
00:35:36  20 of 80 PASS accepted_values_stg_crashes_stats_area__City__Metropolitan__Country  [PASS in 0.02s]
00:35:36  23 of 80 START test assert_release_years_disjoint .............................. [RUN]
00:35:36  22 of 80 PASS assert_month_within_release ...................................... [PASS in 0.02s]
00:35:36  19 of 80 PASS accepted_values_stg_crashes_severity_code__False__1__2__3__4 ..... [PASS in 0.03s]
00:35:36  21 of 80 PASS assert_lga_names_stable_across_releases .......................... [PASS in 0.03s]
00:35:36  24 of 80 START test assert_unit_rows_match_totals .............................. [RUN]
00:35:36  25 of 80 START test non_negative_stg_crashes_total_cas ......................... [RUN]
00:35:36  26 of 80 START test non_negative_stg_crashes_total_fats ........................ [RUN]
00:35:36  23 of 80 PASS assert_release_years_disjoint .................................... [PASS in 0.02s]
00:35:36  27 of 80 START test non_negative_stg_crashes_total_mi .......................... [RUN]
00:35:36  26 of 80 PASS non_negative_stg_crashes_total_fats .............................. [PASS in 0.02s]
00:35:36  28 of 80 START test non_negative_stg_crashes_total_si .......................... [RUN]
00:35:36  25 of 80 PASS non_negative_stg_crashes_total_cas ............................... [PASS in 0.02s]
00:35:36  29 of 80 START test non_negative_stg_crashes_total_units ....................... [RUN]
00:35:36  24 of 80 PASS assert_unit_rows_match_totals .................................... [PASS in 0.03s]
00:35:36  30 of 80 START test not_null_stg_crashes_crash_hour ............................ [RUN]
00:35:36  27 of 80 PASS non_negative_stg_crashes_total_mi ................................ [PASS in 0.02s]
00:35:36  31 of 80 START test not_null_stg_crashes_crash_id .............................. [RUN]
00:35:36  28 of 80 PASS non_negative_stg_crashes_total_si ................................ [PASS in 0.02s]
00:35:36  32 of 80 START test not_null_stg_crashes_crash_month ........................... [RUN]
00:35:36  29 of 80 PASS non_negative_stg_crashes_total_units ............................. [PASS in 0.02s]
00:35:36  33 of 80 START test not_null_stg_crashes_crash_year ............................ [RUN]
00:35:36  30 of 80 PASS not_null_stg_crashes_crash_hour .................................. [PASS in 0.02s]
00:35:36  34 of 80 START test not_null_stg_crashes_lga_name .............................. [RUN]
00:35:36  31 of 80 PASS not_null_stg_crashes_crash_id .................................... [PASS in 0.02s]
00:35:36  35 of 80 START test not_null_stg_crashes_release_id ............................ [RUN]
00:35:36  32 of 80 PASS not_null_stg_crashes_crash_month ................................. [PASS in 0.02s]
00:35:36  36 of 80 START test not_null_stg_crashes_severity_code ......................... [RUN]
00:35:36  33 of 80 PASS not_null_stg_crashes_crash_year .................................. [PASS in 0.02s]
00:35:36  37 of 80 START test relationships_stg_casualties_crash_id__crash_id__ref_stg_crashes_  [RUN]
00:35:36  34 of 80 PASS not_null_stg_crashes_lga_name .................................... [PASS in 0.02s]
00:35:36  38 of 80 START test relationships_stg_crashes_release_id__release_id__source_lake_releases_  [RUN]
00:35:36  35 of 80 PASS not_null_stg_crashes_release_id .................................. [PASS in 0.03s]
00:35:36  39 of 80 START test relationships_stg_crashes_severity_code__severity_code__ref_severity_levels_  [RUN]
00:35:36  36 of 80 PASS not_null_stg_crashes_severity_code ............................... [PASS in 0.02s]
00:35:36  40 of 80 START test relationships_stg_units_crash_id__crash_id__ref_stg_crashes_  [RUN]
00:35:36  38 of 80 PASS relationships_stg_crashes_release_id__release_id__source_lake_releases_  [PASS in 0.02s]
00:35:36  37 of 80 PASS relationships_stg_casualties_crash_id__crash_id__ref_stg_crashes_  [PASS in 0.03s]
00:35:36  41 of 80 START test unique_stg_crashes_crash_id ................................ [RUN]
00:35:36  39 of 80 PASS relationships_stg_crashes_severity_code__severity_code__ref_severity_levels_  [PASS in 0.03s]
00:35:36  41 of 80 PASS unique_stg_crashes_crash_id ...................................... [PASS in 0.02s]
00:35:36  42 of 80 START sql table model main.fct_crashes ................................ [RUN]
00:35:36  40 of 80 PASS relationships_stg_units_crash_id__crash_id__ref_stg_crashes_ ..... [PASS in 0.04s]
00:35:36  42 of 80 OK created sql table model main.fct_crashes ........................... [OK in 0.49s]
00:35:36  43 of 80 START test accepted_values_fct_crashes_severity_code__False__1__2__3__4  [RUN]
00:35:36  44 of 80 START test accepted_values_fct_crashes_severity_name__Property_damage_only__Minor_injury__Serious_injury__Fatal  [RUN]
00:35:36  45 of 80 START test assert_casualty_rows_match_totals .......................... [RUN]
00:35:36  46 of 80 START test assert_fatal_casualties_match_total_fats ................... [RUN]
00:35:36  43 of 80 PASS accepted_values_fct_crashes_severity_code__False__1__2__3__4 ..... [PASS in 0.02s]
00:35:36  45 of 80 PASS assert_casualty_rows_match_totals ................................ [PASS in 0.02s]
00:35:36  46 of 80 PASS assert_fatal_casualties_match_total_fats ......................... [PASS in 0.02s]
00:35:36  44 of 80 PASS accepted_values_fct_crashes_severity_name__Property_damage_only__Minor_injury__Serious_injury__Fatal  [PASS in 0.02s]
00:35:36  47 of 80 START test non_negative_fct_crashes_casualty_rows ..................... [RUN]
00:35:36  48 of 80 START test non_negative_fct_crashes_total_fats ........................ [RUN]
00:35:36  49 of 80 START test not_null_fct_crashes_crash_id .............................. [RUN]
00:35:36  50 of 80 START test not_null_fct_crashes_pdo_regime_id ......................... [RUN]
00:35:36  47 of 80 PASS non_negative_fct_crashes_casualty_rows ........................... [PASS in 0.02s]
00:35:36  48 of 80 PASS non_negative_fct_crashes_total_fats .............................. [PASS in 0.02s]
00:35:36  49 of 80 PASS not_null_fct_crashes_crash_id .................................... [PASS in 0.02s]
00:35:36  50 of 80 PASS not_null_fct_crashes_pdo_regime_id ............................... [PASS in 0.02s]
00:35:36  51 of 80 START test not_null_fct_crashes_severity_code ......................... [RUN]
00:35:36  52 of 80 START test unique_fct_crashes_crash_id ................................ [RUN]
00:35:36  51 of 80 PASS not_null_fct_crashes_severity_code ............................... [PASS in 0.01s]
00:35:36  52 of 80 PASS unique_fct_crashes_crash_id ...................................... [PASS in 0.01s]
00:35:36  53 of 80 START sql table model main.dim_lga .................................... [RUN]
00:35:36  54 of 80 START sql table model main.fct_casualties ............................. [RUN]
00:35:36  55 of 80 START sql table model main.rpt_crash_type_severity .................... [RUN]
00:35:36  56 of 80 START sql table model main.rpt_monthly_severity ....................... [RUN]
00:35:36  53 of 80 OK created sql table model main.dim_lga ............................... [OK in 0.03s]
00:35:36  57 of 80 START sql table model main.rpt_region_fsi ............................. [RUN]
00:35:36  55 of 80 OK created sql table model main.rpt_crash_type_severity ............... [OK in 0.03s]
00:35:36  56 of 80 OK created sql table model main.rpt_monthly_severity .................. [OK in 0.03s]
00:35:36  58 of 80 START test accepted_values_dim_lga_main_stats_area__City__Metropolitan__Country  [RUN]
00:35:36  59 of 80 START test not_null_dim_lga_lga_name .................................. [RUN]
00:35:36  58 of 80 PASS accepted_values_dim_lga_main_stats_area__City__Metropolitan__Country  [PASS in 0.01s]
00:35:36  59 of 80 PASS not_null_dim_lga_lga_name ........................................ [PASS in 0.01s]
00:35:36  60 of 80 START test unique_dim_lga_lga_name .................................... [RUN]
00:35:36  61 of 80 START test non_negative_rpt_crash_type_severity_fsi_crashes ........... [RUN]
00:35:36  57 of 80 OK created sql table model main.rpt_region_fsi ........................ [OK in 0.03s]
00:35:36  62 of 80 START test not_null_rpt_crash_type_severity_crash_type ................ [RUN]
00:35:36  60 of 80 PASS unique_dim_lga_lga_name .......................................... [PASS in 0.02s]
00:35:36  61 of 80 PASS non_negative_rpt_crash_type_severity_fsi_crashes ................. [PASS in 0.02s]
00:35:36  63 of 80 START test unique_rpt_crash_type_severity_crash_type .................. [RUN]
00:35:36  64 of 80 START test non_negative_rpt_monthly_severity_fsi_crashes .............. [RUN]
00:35:36  62 of 80 PASS not_null_rpt_crash_type_severity_crash_type ...................... [PASS in 0.02s]
00:35:36  65 of 80 START test not_null_rpt_monthly_severity_crash_month .................. [RUN]
00:35:36  63 of 80 PASS unique_rpt_crash_type_severity_crash_type ........................ [PASS in 0.02s]
00:35:36  64 of 80 PASS non_negative_rpt_monthly_severity_fsi_crashes .................... [PASS in 0.02s]
00:35:36  66 of 80 START test unique_rpt_monthly_severity_crash_month .................... [RUN]
00:35:36  67 of 80 START test not_null_rpt_region_fsi_stats_area ......................... [RUN]
00:35:36  65 of 80 PASS not_null_rpt_monthly_severity_crash_month ........................ [PASS in 0.01s]
00:35:36  68 of 80 START test unique_rpt_region_fsi_stats_area ........................... [RUN]
00:35:36  54 of 80 OK created sql table model main.fct_casualties ........................ [OK in 0.11s]
00:35:36  69 of 80 START sql table model main.rpt_lga_fsi ................................ [RUN]
00:35:36  66 of 80 PASS unique_rpt_monthly_severity_crash_month .......................... [PASS in 0.02s]
00:35:36  67 of 80 PASS not_null_rpt_region_fsi_stats_area ............................... [PASS in 0.02s]
00:35:36  70 of 80 START test not_null_fct_casualties_crash_id ........................... [RUN]
00:35:36  71 of 80 START test relationships_fct_casualties_crash_id__crash_id__ref_fct_crashes_  [RUN]
00:35:36  68 of 80 PASS unique_rpt_region_fsi_stats_area ................................. [PASS in 0.01s]
00:35:36  72 of 80 START sql table model main.rpt_kpis ................................... [RUN]
00:35:36  70 of 80 PASS not_null_fct_casualties_crash_id ................................. [PASS in 0.02s]
00:35:36  71 of 80 PASS relationships_fct_casualties_crash_id__crash_id__ref_fct_crashes_  [PASS in 0.02s]
00:35:36  73 of 80 START sql table model main.rpt_annual_people .......................... [RUN]
00:35:36  69 of 80 OK created sql table model main.rpt_lga_fsi ........................... [OK in 0.03s]
00:35:36  72 of 80 OK created sql table model main.rpt_kpis .............................. [OK in 0.02s]
00:35:36  74 of 80 START test assert_only_councils_are_ranked ............................ [RUN]
00:35:36  75 of 80 START test not_null_rpt_lga_fsi_lga_name .............................. [RUN]
00:35:36  76 of 80 START test unique_rpt_lga_fsi_lga_name ................................ [RUN]
00:35:36  74 of 80 PASS assert_only_councils_are_ranked .................................. [PASS in 0.01s]
00:35:36  76 of 80 PASS unique_rpt_lga_fsi_lga_name ...................................... [PASS in 0.02s]
00:35:36  75 of 80 PASS not_null_rpt_lga_fsi_lga_name .................................... [PASS in 0.02s]
00:35:36  73 of 80 OK created sql table model main.rpt_annual_people ..................... [OK in 0.02s]
00:35:36  77 of 80 START test non_negative_rpt_annual_people_admitted_to_hospital ........ [RUN]
00:35:36  78 of 80 START test non_negative_rpt_annual_people_fatalities .................. [RUN]
00:35:36  79 of 80 START test not_null_rpt_annual_people_crash_year ...................... [RUN]
00:35:36  80 of 80 START test unique_rpt_annual_people_crash_year ........................ [RUN]
00:35:36  77 of 80 PASS non_negative_rpt_annual_people_admitted_to_hospital .............. [PASS in 0.02s]
00:35:36  78 of 80 PASS non_negative_rpt_annual_people_fatalities ........................ [PASS in 0.02s]
00:35:36  79 of 80 PASS not_null_rpt_annual_people_crash_year ............................ [PASS in 0.02s]
00:35:36  80 of 80 PASS unique_rpt_annual_people_crash_year .............................. [PASS in 0.02s]
00:35:36  
00:35:36  Finished running 3 seeds, 9 table models, 64 data tests, 4 view models in 0 hours 0 minutes and 1.08 seconds (1.08s).
00:35:36  
00:35:36  Completed successfully
00:35:36  
00:35:36  Done. PASS=80 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=80
11:05:38.601 | INFO    | Task run 'dbt_build-397' - dbt build finished: pass=64, success=16
11:05:38.602 | INFO    | Task run 'dbt_build-397' - Finished in state Completed()
11:05:38.708 | INFO    | Task run 'benchmark_warehouse-d4d' - 
EXPLAIN ANALYZE (tile2_monthly_fsi_2021_2025, curated layout)
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││    Query Profiling Information    ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
explain analyze select crash_month, count(*) filter (where is_fsi) as fsi_crashes from read_parquet('/private/tmp/de-w7-fix/original/project/data/lake/curated/fct_crashes/*/*.parquet', hive_partitioning=true) where crash_year between 2021 and 2025 group by crash_month order by crash_month
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 0.0014s             ││
│└──────────────────────────────────────────────┘│
└────────────────────────────────────────────────┘
┌───────────────────────────┐
│           QUERY           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      EXPLAIN_ANALYZE      │
│    ────────────────────   │
│                           │
│           0 rows          │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│          ORDER_BY         │
│    ────────────────────   │
│  read_parquet.crash_month │
│             ASC           │
│                           │
│                           │
│                           │
│          60 rows          │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│         Groups: #0        │
│                           │
│        Aggregates:        │
│ count_star() FILTER (WHERE│
│       #0) Filter: #0      │
│                           │
│                           │
│                           │
│          60 rows          │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        crash_month        │
│           is_fsi          │
│                           │
│                           │
│                           │
│        65,655 rows        │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         TABLE_SCAN        │
│    ────────────────────   │
│         Function:         │
│        READ_PARQUET       │
│                           │
│        Projections:       │
│        crash_month        │
│           is_fsi          │
│                           │
│       File Filters:       │
│  (crash_year BETWEEN 2021 │
│          AND 2025)        │
│                           │
│    Scanning Files: 5/14   │
│    Total Files Read: 5    │
│                           │
│        Filename(s):       │
│   /private/tmp/de-w7-fix  │
│   /original/project/data  │
│ /lake/curated/fct_crashes │
│  /crash_year=2021/part_0  │
│ .parquet, /private/tmp/de │
│  -w7-fix/original/project │
│     /data/lake/curated    │
│  /fct_crashes/crash_year  │
│   =2022/part_0.parquet,   │
│   /private/tmp/de-w7-fix  │
│   /original/project/data  │
│ /lake/curated/fct_crashes │
│  /crash_year=2023/part_0  │
│ .parquet, /private/tmp/de │
│  -w7-fix/original/project │
│     /data/lake/curated    │
│  /fct_crashes/crash_year  │
│   =2024/part_0.parquet,   │
│   /private/tmp/de-w7-fix  │
│   /original/project/data  │
│ /lake/curated/fct_crashes │
│  /crash_year=2025/part_0  │
│          .parquet         │
│                           │
│                           │
│                           │
│        65,655 rows        │
│           0.00s           │
└───────────────────────────┘
11:05:38.727 | INFO    | Task run 'benchmark_warehouse-d4d' - 
EXPLAIN ANALYZE (tile1_crash_type_fsi_2024, curated layout)
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││    Query Profiling Information    ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
explain analyze select crash_type, count(*) as fsi_crashes from read_parquet('/private/tmp/de-w7-fix/original/project/data/lake/curated/fct_crashes/*/*.parquet', hive_partitioning=true) where crash_year = 2024 and severity_code >= 3 group by crash_type order by crash_type
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 0.0010s             ││
│└──────────────────────────────────────────────┘│
└────────────────────────────────────────────────┘
┌───────────────────────────┐
│           QUERY           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      EXPLAIN_ANALYZE      │
│    ────────────────────   │
│                           │
│           0 rows          │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│          ORDER_BY         │
│    ────────────────────   │
│read_parquet.crash_type ASC│
│                           │
│                           │
│                           │
│          13 rows          │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│         Groups: #0        │
│                           │
│        Aggregates:        │
│        count_star()       │
│                           │
│                           │
│                           │
│          13 rows          │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│         crash_type        │
│                           │
│                           │
│                           │
│          864 rows         │
│           0.00s           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         TABLE_SCAN        │
│    ────────────────────   │
│         Function:         │
│        READ_PARQUET       │
│                           │
│        Projections:       │
│         crash_type        │
│                           │
│          Filters:         │
│      severity_code>=3     │
│                           │
│       File Filters:       │
│    (crash_year = 2024)    │
│                           │
│    Scanning Files: 1/14   │
│    Total Files Read: 1    │
│                           │
│        Filename(s):       │
│   /private/tmp/de-w7-fix  │
│   /original/project/data  │
│ /lake/curated/fct_crashes │
│  /crash_year=2024/part_0  │
│          .parquet         │
│                           │
│                           │
│                           │
│          864 rows         │
│           0.00s           │
└───────────────────────────┘
11:05:38.747 | INFO    | Task run 'benchmark_warehouse-d4d' - 
Partitioning and clustering benchmark (same rows, 8,192-row row groups)
11:05:38.747 | INFO    | Task run 'benchmark_warehouse-d4d' - query                              layout       files   row groups     rows to read  median ms
11:05:38.747 | INFO    | Task run 'benchmark_warehouse-d4d' - ----------------------------------------------------------------------------------------------
11:05:38.747 | INFO    | Task run 'benchmark_warehouse-d4d' - tile2_monthly_fsi_2021_2025        flat           1/1        10/26     73788/204860       1.39
11:05:38.747 | INFO    | Task run 'benchmark_warehouse-d4d' - tile2_monthly_fsi_2021_2025        curated       5/14        10/31     65655/204860       1.07
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' -                                    same result on both layouts: True
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' - tile1_crash_type_fsi_2024          flat           1/1         3/26     24576/204860       1.13
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' - tile1_crash_type_fsi_2024          curated       1/14         2/31     13140/204860       0.78
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' -                                    same result on both layouts: True
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' - lga_drilldown_adelaide_q1_2024     flat           1/1         2/26     16384/204860       0.99
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' - lga_drilldown_adelaide_q1_2024     curated      14/14         1/31      8192/204860       1.06
11:05:38.748 | INFO    | Task run 'benchmark_warehouse-d4d' -                                    same result on both layouts: True
11:05:38.749 | INFO    | Task run 'benchmark_warehouse-d4d' - 
benchmark written to /private/tmp/de-w7-fix/original/project/data/warehouse/benchmark.json
11:05:38.750 | INFO    | Task run 'benchmark_warehouse-d4d' - Finished in state Completed()
11:05:38.763 | INFO    | Task run 'export_dashboard-00c' - exported 168 months, 13 crash types; crashes=204860 fsi_crashes=10204 fatalities=1337 serious_injuries=10435
11:05:38.764 | INFO    | Task run 'export_dashboard-00c' - 
Dashboard summary (from the exported JSON)
FSI crashes by crash type:
   1. Hit Fixed Object             fsi= 2674 fatal= 393 serious= 2281 share_of_fsi=26.21% crashes= 31722 fsi_pct_of_casualty_crashes=26.99%
   2. Roll Over                    fsi= 1615 fatal= 178 serious= 1437 share_of_fsi=15.83% crashes=  8685 fsi_pct_of_casualty_crashes=30.36%
   3. Right Angle                  fsi= 1474 fatal= 137 serious= 1337 share_of_fsi=14.45% crashes= 40214 fsi_pct_of_casualty_crashes=11.37%
   4. Hit Pedestrian               fsi= 1097 fatal= 185 serious=  912 share_of_fsi=10.75% crashes=  5214 fsi_pct_of_casualty_crashes=28.66%
   5. Rear End                     fsi=  738 fatal=  55 serious=  683 share_of_fsi= 7.23% crashes= 55141 fsi_pct_of_casualty_crashes=4.1%
   6. Right Turn                   fsi=  731 fatal=  35 serious=  696 share_of_fsi= 7.16% crashes= 16721 fsi_pct_of_casualty_crashes=11.74%
   7. Head On                      fsi=  661 fatal= 169 serious=  492 share_of_fsi= 6.48% crashes=  3442 fsi_pct_of_casualty_crashes=38.39%
   8. Side Swipe                   fsi=  498 fatal=  40 serious=  458 share_of_fsi= 4.88% crashes= 21191 fsi_pct_of_casualty_crashes=11.57%
   9. Hit Parked Vehicle           fsi=  317 fatal=  16 serious=  301 share_of_fsi= 3.11% crashes= 15435 fsi_pct_of_casualty_crashes=13.11%
  10. Hit Animal                   fsi=  149 fatal=  16 serious=  133 share_of_fsi= 1.46% crashes=  3235 fsi_pct_of_casualty_crashes=28.06%
  11. Left Road - Out of Control   fsi=  108 fatal=   4 serious=  104 share_of_fsi= 1.06% crashes=  1633 fsi_pct_of_casualty_crashes=20.89%
  12. Other                        fsi=   81 fatal=  10 serious=   71 share_of_fsi= 0.79% crashes=  1410 fsi_pct_of_casualty_crashes=23.82%
  13. Hit Object on Road           fsi=   61 fatal=   3 serious=   58 share_of_fsi=  0.6% crashes=   817 fsi_pct_of_casualty_crashes=29.33%
People per year (casualty rows):
  2012: lives_lost= 94 admitted_to_hospital= 761 fsi_crashes= 723 crashes= 22829
  2013: lives_lost= 97 admitted_to_hospital= 790 fsi_crashes= 755 crashes= 16675
  2014: lives_lost=108 admitted_to_hospital= 711 fsi_crashes= 690 crashes= 16162
  2015: lives_lost=102 admitted_to_hospital= 759 fsi_crashes= 753 crashes= 15431
  2016: lives_lost= 86 admitted_to_hospital= 692 fsi_crashes= 651 crashes= 16775
  2017: lives_lost=100 admitted_to_hospital= 622 fsi_crashes= 626 crashes= 13236
  2018: lives_lost= 80 admitted_to_hospital= 576 fsi_crashes= 560 crashes= 13599
  2019: lives_lost=114 admitted_to_hospital= 833 fsi_crashes= 839 crashes= 12964
  2020: lives_lost= 93 admitted_to_hospital= 715 fsi_crashes= 709 crashes= 11534
  2021: lives_lost= 99 admitted_to_hospital= 827 fsi_crashes= 810 crashes= 13149
  2022: lives_lost= 71 admitted_to_hospital= 652 fsi_crashes= 643 crashes= 12356
  2023: lives_lost=117 admitted_to_hospital= 824 fsi_crashes= 821 crashes= 13066
  2024: lives_lost= 89 admitted_to_hospital= 908 fsi_crashes= 864 crashes= 13140
  2025: lives_lost= 87 admitted_to_hospital= 765 fsi_crashes= 760 crashes= 13944 provisional
FSI crashes by statistical area:
  Metropolitan  fsi= 5891 share_of_fsi=57.73% crashes=162545 fsi_pct_of_casualty_crashes=11.58%
  Country       fsi= 3973 share_of_fsi=38.94% crashes= 31941 fsi_pct_of_casualty_crashes=32.51%
  City          fsi=  340 share_of_fsi=3.33% crashes= 10374 fsi_pct_of_casualty_crashes=10.72%
Top council areas by FSI crashes (councils only):
   1. CITY OF ONKAPARINGA              fsi= 728 fatal= 60 crashes= 13875 main_area=Metropolitan
   2. THE ADELAIDE HILLS COUNCIL       fsi= 583 fatal= 61 crashes=  6312 main_area=Metropolitan
   3. CITY OF PORT ADELAIDE ENFIELD    fsi= 564 fatal= 49 crashes= 19106 main_area=Metropolitan
   4. CITY OF SALISBURY                fsi= 559 fatal= 63 crashes= 17924 main_area=Metropolitan
   5. CITY OF PLAYFORD                 fsi= 522 fatal= 63 crashes= 11733 main_area=Metropolitan
   6. CITY OF CHARLES STURT            fsi= 435 fatal= 38 crashes= 14700 main_area=Metropolitan
   7. CITY OF ADELAIDE                 fsi= 340 fatal= 15 crashes= 10371 main_area=City
   8. CC MARION                        fsi= 338 fatal= 21 crashes= 10552 main_area=Metropolitan
   9. CITY OF WEST TORRENS             fsi= 323 fatal= 25 crashes= 11220 main_area=Metropolitan
  10. CC MITCHAM                       fsi= 307 fatal= 27 crashes=  9507 main_area=Metropolitan
Not ranked (not a council):
      UNINCORPORATED OR UNKNOWN        fsi= 375 fatal= 72 crashes=  1665 main_area=Country stats_areas=1
      UNINCORP (EASTERN)               fsi=   1 fatal=  0 crashes=    10 main_area=Country stats_areas=1
      UNINCORP (NORTHERN & WESTERN)    fsi=   1 fatal=  1 crashes=    35 main_area=Country stats_areas=1
      METRO UNINCORPORATED             fsi=   0 fatal=  0 crashes=     4 main_area=Metropolitan stats_areas=1
Monthly FSI: peak month 2024-03 (96); 12-month mean lowest 46.17 (to 2018-10), highest 73.25 (to 2024-08)
11:05:38.764 | INFO    | Task run 'export_dashboard-00c' - dashboard JSON written to /private/tmp/de-w7-fix/web/app/project/dashboard-data.json (70702 bytes)
11:05:38.765 | INFO    | Task run 'export_dashboard-00c' - Finished in state Completed()
11:05:39.550 | INFO    | Flow run 'visionary-dolphin' - Finished in state Completed()
11:05:39.560 | INFO    | prefect - Stopping temporary server on http://127.0.0.1:8078
/Applications/Xcode.app/Contents/Developer/usr/bin/make test
.venv/bin/python -m pytest -m "not integration" -v
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.1.1, pluggy-1.7.0 -- /private/tmp/de-w7-fix/original/project/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/tmp/de-w7-fix/original/project
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collecting ... collected 44 items / 18 deselected / 26 selected

tests/test_dbt_fixture.py::test_dbt_build_passes_on_the_fixture PASSED   [  3%]
tests/test_ingest.py::test_fetch_downloads_verifies_and_then_reuses_the_cache PASSED [  7%]
tests/test_ingest.py::test_checksum_mismatch_fails_and_leaves_nothing_behind PASSED [ 11%]
tests/test_ingest.py::test_cached_file_with_wrong_bytes_is_downloaded_again PASSED [ 15%]
tests/test_ingest.py::test_404_fails_fast_without_retrying PASSED        [ 19%]
tests/test_ingest.py::test_5xx_is_retried_with_backoff_then_gives_up PASSED [ 23%]
tests/test_ingest.py::test_transient_5xx_recovers PASSED                 [ 26%]
tests/test_ingest.py::test_unreachable_host_raises_unavailable PASSED    [ 30%]
tests/test_ingest.py::test_fixture_releases_pass_the_schema_contract PASSED [ 34%]
tests/test_ingest.py::test_missing_column_breaks_the_contract PASSED     [ 38%]
tests/test_ingest.py::test_crash_outside_release_years_breaks_the_contract PASSED [ 42%]
tests/test_ingest.py::test_zip_without_casualty_csv_is_rejected PASSED   [ 46%]
tests/test_ingest.py::test_load_writes_hive_partitions_with_lineage PASSED [ 50%]
tests/test_ingest.py::test_lake_types_are_cast PASSED                    [ 53%]
tests/test_ingest.py::test_reloading_a_release_is_idempotent PASSED      [ 57%]
tests/test_ingest.py::test_new_extract_replaces_only_its_own_years PASSED [ 61%]
tests/test_ingest.py::test_prune_removes_years_no_release_covers PASSED  [ 65%]
tests/test_ingest.py::test_release_manifest_is_stored_in_the_lake PASSED [ 69%]
tests/test_sources.py::test_repo_manifest_covers_2012_to_2025_without_gaps PASSED [ 73%]
tests/test_sources.py::test_repo_manifest_urls_point_at_data_sa PASSED   [ 76%]
tests/test_sources.py::test_repo_manifest_records_licence_and_attribution PASSED [ 80%]
tests/test_sources.py::test_overlapping_years_are_rejected PASSED        [ 84%]
tests/test_sources.py::test_gap_in_years_is_rejected PASSED              [ 88%]
tests/test_sources.py::test_malformed_checksum_is_rejected PASSED        [ 92%]
tests/test_sources.py::test_duplicate_release_ids_are_rejected PASSED    [ 96%]
tests/test_sources.py::test_missing_keys_are_rejected PASSED             [100%]

====================== 26 passed, 18 deselected in 7.75s =======================
.venv/bin/python -m pytest -m integration -v
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.1.1, pluggy-1.7.0 -- /private/tmp/de-w7-fix/original/project/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/tmp/de-w7-fix/original/project
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collecting ... collected 44 items / 26 deselected / 18 selected

tests/test_dashboard_export.py::test_dashboard_has_at_least_two_tiles PASSED [  5%]
tests/test_dashboard_export.py::test_months_are_continuous_from_2012_to_2025 PASSED [ 11%]
tests/test_dashboard_export.py::test_rolling_mean_is_the_trailing_twelve_month_average PASSED [ 16%]
tests/test_dashboard_export.py::test_totals_reconcile_with_the_warehouse PASSED [ 22%]
tests/test_dashboard_export.py::test_council_ranking_holds_only_councils PASSED [ 27%]
tests/test_dashboard_export.py::test_crash_types_are_sorted_by_fsi PASSED [ 33%]
tests/test_dashboard_export.py::test_only_the_latest_year_is_provisional PASSED [ 38%]
tests/test_dashboard_export.py::test_export_is_deterministic_and_matches_the_committed_file PASSED [ 44%]
tests/test_dashboard_export.py::test_attribution_and_release_dates_travel_with_the_data PASSED [ 50%]
tests/test_dashboard_export.py::test_2023_matches_the_published_road_safety_annual_report PASSED [ 55%]
tests/test_warehouse.py::test_lake_has_one_partition_per_year_for_every_table PASSED [ 61%]
tests/test_warehouse.py::test_row_counts_carry_through_from_lake_to_warehouse PASSED [ 66%]
tests/test_warehouse.py::test_lake_counts_match_the_crash_totals PASSED  [ 72%]
tests/test_warehouse.py::test_fct_crashes_is_stored_in_cluster_order PASSED [ 77%]
tests/test_warehouse.py::test_curated_export_is_partitioned_with_small_sorted_row_groups PASSED [ 83%]
tests/test_warehouse.py::test_every_dbt_node_passed PASSED               [ 88%]
tests/test_warehouse.py::test_benchmark_shows_less_data_to_read_on_the_curated_layout PASSED [ 94%]
tests/test_warehouse.py::test_lga_aliases_leave_no_trailing_full_stops PASSED [100%]

====================== 18 passed, 26 deselected in 0.66s =======================
make all finished in 239s
$ du -sh data/landing data/lake/raw data/lake/curated data/warehouse/sa_crash.duckdb
 19M	data/landing
8.9M	data/lake/raw
4.3M	data/lake/curated
 12M	data/warehouse/sa_crash.duckdb
```
