# Run log

Real terminal output of `scripts/run_all.sh` (which runs `make all`) on the machine
and date shown below. Nothing here is edited except that this header was added.

```text
$ date -u
Mon Oct 19 23:59:02 UTC 2026
$ uname -sm
Darwin arm64
$ .venv/bin/python --version
Python 3.11.14
$ rm -rf data/landing data/lake data/warehouse dbt/target
$ ls -l data/landing
(empty: first run downloads every release)
$ make all
.venv/bin/python -m pipeline.flow
10:29:06.312 | INFO    | prefect - Starting temporary server on http://127.0.0.1:8743
See https://docs.prefect.io/v3/concepts/server#how-to-guides for more information on running a dedicated Prefect server.
10:29:09.332 | INFO    | Flow run 'jade-crab' - Beginning flow run 'jade-crab' for flow 'sa_crash_pipeline'
10:29:09.337 | INFO    | Flow run 'jade-crab' - manifest: 10 releases covering 2012-2025 (14 years)
10:29:11.679 | INFO    | Task run 'fetch_release-143' - sa_crash_2012_as_at_20210527: downloaded 2012_data_sa_as_at_20210527.zip (1628505 bytes, sha256 02380fee078e...)
10:29:11.681 | INFO    | Task run 'fetch_release-143' - Finished in state Completed()
10:29:11.856 | INFO    | Task run 'validate_schema-8d7' - sa_crash_2012_as_at_20210527: header contract ok; rows crash=22829 casualty=7479 units=48320
10:29:11.857 | INFO    | Task run 'validate_schema-8d7' - Finished in state Completed()
10:29:12.135 | INFO    | Task run 'load_to_lake-31a' - sa_crash_2012_as_at_20210527: wrote years 2012-2012 to lake; crash=22829 casualty=7479 units=48320
10:29:12.136 | INFO    | Task run 'load_to_lake-31a' - Finished in state Completed()
10:29:12.564 | INFO    | Task run 'fetch_release-126' - sa_crash_2013_as_at_20210527: downloaded 2013_data_sa_as_at_20210527.zip (1257991 bytes, sha256 697e5ae5b0dd...)
10:29:12.567 | INFO    | Task run 'fetch_release-126' - Finished in state Completed()
10:29:12.710 | INFO    | Task run 'validate_schema-3ef' - sa_crash_2013_as_at_20210527: header contract ok; rows crash=16675 casualty=7177 units=35865
10:29:12.711 | INFO    | Task run 'validate_schema-3ef' - Finished in state Completed()
10:29:12.925 | INFO    | Task run 'load_to_lake-e9f' - sa_crash_2013_as_at_20210527: wrote years 2013-2013 to lake; crash=16675 casualty=7177 units=35865
10:29:12.926 | INFO    | Task run 'load_to_lake-e9f' - Finished in state Completed()
10:29:13.337 | INFO    | Task run 'fetch_release-3e0' - sa_crash_2014_as_at_20210527: downloaded 2014_data_sa_as_at_20210527.zip (1221928 bytes, sha256 d6ff9170c6ef...)
10:29:13.341 | INFO    | Task run 'fetch_release-3e0' - Finished in state Completed()
10:29:13.486 | INFO    | Task run 'validate_schema-cd1' - sa_crash_2014_as_at_20210527: header contract ok; rows crash=16162 casualty=6982 units=34552
10:29:13.487 | INFO    | Task run 'validate_schema-cd1' - Finished in state Completed()
10:29:13.701 | INFO    | Task run 'load_to_lake-7dc' - sa_crash_2014_as_at_20210527: wrote years 2014-2014 to lake; crash=16162 casualty=6982 units=34552
10:29:13.702 | INFO    | Task run 'load_to_lake-7dc' - Finished in state Completed()
10:29:14.105 | INFO    | Task run 'fetch_release-585' - sa_crash_2015_as_at_20210527: downloaded 2015_data_sa_as_at_20210527.zip (1168394 bytes, sha256 8aa9d4b9bca0...)
10:29:14.107 | INFO    | Task run 'fetch_release-585' - Finished in state Completed()
10:29:14.228 | INFO    | Task run 'validate_schema-472' - sa_crash_2015_as_at_20210527: header contract ok; rows crash=15431 casualty=6660 units=33084
10:29:14.229 | INFO    | Task run 'validate_schema-472' - Finished in state Completed()
10:29:14.433 | INFO    | Task run 'load_to_lake-b7b' - sa_crash_2015_as_at_20210527: wrote years 2015-2015 to lake; crash=15431 casualty=6660 units=33084
10:29:14.433 | INFO    | Task run 'load_to_lake-b7b' - Finished in state Completed()
10:29:14.851 | INFO    | Task run 'fetch_release-191' - sa_crash_2016_as_at_20210527: downloaded 2016_data_sa_as_at_20210527.zip (1259179 bytes, sha256 3d1ce02ebe9d...)
10:29:14.852 | INFO    | Task run 'fetch_release-191' - Finished in state Completed()
10:29:15.014 | INFO    | Task run 'validate_schema-a52' - sa_crash_2016_as_at_20210527: header contract ok; rows crash=16775 casualty=6565 units=35861
10:29:15.015 | INFO    | Task run 'validate_schema-a52' - Finished in state Completed()
10:29:15.230 | INFO    | Task run 'load_to_lake-533' - sa_crash_2016_as_at_20210527: wrote years 2016-2016 to lake; crash=16775 casualty=6565 units=35861
10:29:15.231 | INFO    | Task run 'load_to_lake-533' - Finished in state Completed()
10:29:16.007 | INFO    | Task run 'fetch_release-219' - sa_crash_2017_as_at_20210527: downloaded 2017_data_sa_as_at_20210527.zip (1001803 bytes, sha256 a97b3c4e877c...)
10:29:16.010 | INFO    | Task run 'fetch_release-219' - Finished in state Completed()
10:29:16.133 | INFO    | Task run 'validate_schema-247' - sa_crash_2017_as_at_20210527: header contract ok; rows crash=13236 casualty=6237 units=28161
10:29:16.134 | INFO    | Task run 'validate_schema-247' - Finished in state Completed()
10:29:16.316 | INFO    | Task run 'load_to_lake-00f' - sa_crash_2017_as_at_20210527: wrote years 2017-2017 to lake; crash=13236 casualty=6237 units=28161
10:29:16.317 | INFO    | Task run 'load_to_lake-00f' - Finished in state Completed()
10:29:18.146 | INFO    | Task run 'fetch_release-d27' - sa_crash_2018_as_at_20210527: downloaded 2018_data_sa_as_at_20210527.zip (1024690 bytes, sha256 c7fad62e2f7b...)
10:29:18.149 | INFO    | Task run 'fetch_release-d27' - Finished in state Completed()
10:29:18.284 | INFO    | Task run 'validate_schema-097' - sa_crash_2018_as_at_20210527: header contract ok; rows crash=13599 casualty=6124 units=29033
10:29:18.285 | INFO    | Task run 'validate_schema-097' - Finished in state Completed()
10:29:18.471 | INFO    | Task run 'load_to_lake-35c' - sa_crash_2018_as_at_20210527: wrote years 2018-2018 to lake; crash=13599 casualty=6124 units=29033
10:29:18.472 | INFO    | Task run 'load_to_lake-35c' - Finished in state Completed()
10:29:19.203 | INFO    | Task run 'fetch_release-ad7' - sa_crash_2019_as_at_20210527: downloaded 2019_data_sa_as_at_20210527.zip (980081 bytes, sha256 aef9a66aef27...)
10:29:19.204 | INFO    | Task run 'fetch_release-ad7' - Finished in state Completed()
10:29:19.319 | INFO    | Task run 'validate_schema-f49' - sa_crash_2019_as_at_20210527: header contract ok; rows crash=12964 casualty=6031 units=27714
10:29:19.320 | INFO    | Task run 'validate_schema-f49' - Finished in state Completed()
10:29:19.505 | INFO    | Task run 'load_to_lake-702' - sa_crash_2019_as_at_20210527: wrote years 2019-2019 to lake; crash=12964 casualty=6031 units=27714
10:29:19.506 | INFO    | Task run 'load_to_lake-702' - Finished in state Completed()
10:29:20.226 | INFO    | Task run 'fetch_release-fbe' - sa_crash_2020_as_at_20210527: downloaded 2020_data_sa_as_at_20210527.zip (865285 bytes, sha256 8a5f4269d900...)
10:29:20.229 | INFO    | Task run 'fetch_release-fbe' - Finished in state Completed()
10:29:20.355 | INFO    | Task run 'validate_schema-74c' - sa_crash_2020_as_at_20210527: header contract ok; rows crash=11534 casualty=4877 units=24539
10:29:20.357 | INFO    | Task run 'validate_schema-74c' - Finished in state Completed()
10:29:20.525 | INFO    | Task run 'load_to_lake-18c' - sa_crash_2020_as_at_20210527: wrote years 2020-2020 to lake; crash=11534 casualty=4877 units=24539
10:29:20.526 | INFO    | Task run 'load_to_lake-18c' - Finished in state Completed()
10:29:22.109 | INFO    | Task run 'fetch_release-cd4' - sa_crash_2021_2025_as_at_20261009: downloaded 2021-2025_data_sa_crash_as_at_20261009.zip (5155745 bytes, sha256 2c6df4a4bcae...)
10:29:22.110 | INFO    | Task run 'fetch_release-cd4' - Finished in state Completed()
10:29:22.385 | INFO    | Task run 'validate_schema-7bb' - sa_crash_2021_2025_as_at_20261009: header contract ok; rows crash=65655 casualty=23751 units=140150
10:29:22.386 | INFO    | Task run 'validate_schema-7bb' - Finished in state Completed()
10:29:22.907 | INFO    | Task run 'load_to_lake-30a' - sa_crash_2021_2025_as_at_20261009: wrote years 2021-2025 to lake; crash=65655 casualty=23751 units=140150
10:29:22.908 | INFO    | Task run 'load_to_lake-30a' - Finished in state Completed()
10:29:22.931 | INFO    | Flow run 'jade-crab' - lake has 14 crash year partitions (2012-2025); removed 0 stale
23:59:23  Running with dbt=1.12.6
23:59:23  Registered adapter: duckdb=1.11.0
23:59:23  Unable to do partial parsing because saved manifest not found. Starting full parse.
23:59:24  Found 13 models, 63 data tests, 3 seeds, 4 sources, 501 macros
23:59:24  
23:59:24  Concurrency: 4 threads (target='dev')
23:59:24  
23:59:24  1 of 79 START sql view model main.stg_casualties ............................... [RUN]
23:59:24  2 of 79 START sql view model main.stg_units .................................... [RUN]
23:59:24  3 of 79 START seed file main.lga_name_aliases .................................. [RUN]
23:59:24  4 of 79 START seed file main.pdo_reporting_regimes ............................. [RUN]
23:59:24  3 of 79 OK loaded seed file main.lga_name_aliases .............................. [INSERT 33 in 0.05s]
23:59:24  4 of 79 OK loaded seed file main.pdo_reporting_regimes ......................... [INSERT 4 in 0.05s]
23:59:24  5 of 79 START seed file main.severity_levels ................................... [RUN]
23:59:24  6 of 79 START test not_null_lga_name_aliases_raw_lga_name ...................... [RUN]
23:59:24  2 of 79 OK created sql view model main.stg_units ............................... [OK in 0.06s]
23:59:24  1 of 79 OK created sql view model main.stg_casualties .......................... [OK in 0.06s]
23:59:24  7 of 79 START test unique_lga_name_aliases_raw_lga_name ........................ [RUN]
23:59:24  8 of 79 START test not_null_pdo_reporting_regimes_regime_id .................... [RUN]
23:59:24  6 of 79 PASS not_null_lga_name_aliases_raw_lga_name ............................ [PASS in 0.03s]
23:59:24  9 of 79 START test unique_pdo_reporting_regimes_regime_id ...................... [RUN]
23:59:24  7 of 79 PASS unique_lga_name_aliases_raw_lga_name .............................. [PASS in 0.03s]
23:59:24  5 of 79 OK loaded seed file main.severity_levels ............................... [INSERT 4 in 0.03s]
23:59:24  8 of 79 PASS not_null_pdo_reporting_regimes_regime_id .......................... [PASS in 0.03s]
23:59:24  10 of 79 START test non_negative_stg_units_casualties_in_unit .................. [RUN]
23:59:24  11 of 79 START test not_null_stg_units_crash_id ................................ [RUN]
23:59:24  12 of 79 START test accepted_values_stg_casualties_injury_extent__Fatal__Admitted_to_Hospital__Treated_at_Hospital__By_Private  [RUN]
23:59:24  9 of 79 PASS unique_pdo_reporting_regimes_regime_id ............................ [PASS in 0.02s]
23:59:24  13 of 79 START test non_negative_stg_casualties_age ............................ [RUN]
23:59:24  12 of 79 PASS accepted_values_stg_casualties_injury_extent__Fatal__Admitted_to_Hospital__Treated_at_Hospital__By_Private  [PASS in 0.03s]
23:59:24  11 of 79 PASS not_null_stg_units_crash_id ...................................... [PASS in 0.03s]
23:59:24  10 of 79 PASS non_negative_stg_units_casualties_in_unit ........................ [PASS in 0.03s]
23:59:24  14 of 79 START test not_null_stg_casualties_crash_id ........................... [RUN]
23:59:24  15 of 79 START sql view model main.stg_crashes ................................. [RUN]
23:59:24  16 of 79 START test not_null_severity_levels_severity_code ..................... [RUN]
23:59:24  13 of 79 PASS non_negative_stg_casualties_age .................................. [PASS in 0.02s]
23:59:24  17 of 79 START test unique_severity_levels_severity_code ....................... [RUN]
23:59:24  16 of 79 PASS not_null_severity_levels_severity_code ........................... [PASS in 0.02s]
23:59:24  14 of 79 PASS not_null_stg_casualties_crash_id ................................. [PASS in 0.02s]
23:59:24  18 of 79 START sql view model main.int_casualty_counts ......................... [RUN]
23:59:24  17 of 79 PASS unique_severity_levels_severity_code ............................. [PASS in 0.01s]
23:59:24  15 of 79 OK created sql view model main.stg_crashes ............................ [OK in 0.03s]
23:59:24  19 of 79 START test accepted_values_stg_crashes_severity_code__False__1__2__3__4  [RUN]
23:59:24  20 of 79 START test accepted_values_stg_crashes_stats_area__City__Metropolitan__Country  [RUN]
23:59:24  21 of 79 START test assert_lga_names_stable_across_releases .................... [RUN]
23:59:24  18 of 79 OK created sql view model main.int_casualty_counts .................... [OK in 0.02s]
23:59:24  22 of 79 START test assert_month_within_release ................................ [RUN]
23:59:24  19 of 79 PASS accepted_values_stg_crashes_severity_code__False__1__2__3__4 ..... [PASS in 0.02s]
23:59:24  23 of 79 START test assert_release_years_disjoint .............................. [RUN]
23:59:24  20 of 79 PASS accepted_values_stg_crashes_stats_area__City__Metropolitan__Country  [PASS in 0.02s]
23:59:24  21 of 79 PASS assert_lga_names_stable_across_releases .......................... [PASS in 0.03s]
23:59:24  24 of 79 START test assert_unit_rows_match_totals .............................. [RUN]
23:59:24  25 of 79 START test non_negative_stg_crashes_total_cas ......................... [RUN]
23:59:24  22 of 79 PASS assert_month_within_release ...................................... [PASS in 0.03s]
23:59:24  25 of 79 PASS non_negative_stg_crashes_total_cas ............................... [PASS in 0.02s]
23:59:24  23 of 79 PASS assert_release_years_disjoint .................................... [PASS in 0.03s]
23:59:24  26 of 79 START test non_negative_stg_crashes_total_fats ........................ [RUN]
23:59:24  27 of 79 START test non_negative_stg_crashes_total_mi .......................... [RUN]
23:59:24  28 of 79 START test non_negative_stg_crashes_total_si .......................... [RUN]
23:59:24  24 of 79 PASS assert_unit_rows_match_totals .................................... [PASS in 0.03s]
23:59:24  29 of 79 START test non_negative_stg_crashes_total_units ....................... [RUN]
23:59:24  26 of 79 PASS non_negative_stg_crashes_total_fats .............................. [PASS in 0.02s]
23:59:24  27 of 79 PASS non_negative_stg_crashes_total_mi ................................ [PASS in 0.03s]
23:59:24  28 of 79 PASS non_negative_stg_crashes_total_si ................................ [PASS in 0.03s]
23:59:24  30 of 79 START test not_null_stg_crashes_crash_hour ............................ [RUN]
23:59:24  31 of 79 START test not_null_stg_crashes_crash_id .............................. [RUN]
23:59:24  32 of 79 START test not_null_stg_crashes_crash_month ........................... [RUN]
23:59:24  29 of 79 PASS non_negative_stg_crashes_total_units ............................. [PASS in 0.02s]
23:59:24  33 of 79 START test not_null_stg_crashes_crash_year ............................ [RUN]
23:59:24  31 of 79 PASS not_null_stg_crashes_crash_id .................................... [PASS in 0.02s]
23:59:24  34 of 79 START test not_null_stg_crashes_lga_name .............................. [RUN]
23:59:24  30 of 79 PASS not_null_stg_crashes_crash_hour .................................. [PASS in 0.03s]
23:59:24  33 of 79 PASS not_null_stg_crashes_crash_year .................................. [PASS in 0.02s]
23:59:24  32 of 79 PASS not_null_stg_crashes_crash_month ................................. [PASS in 0.02s]
23:59:24  35 of 79 START test not_null_stg_crashes_release_id ............................ [RUN]
23:59:24  36 of 79 START test not_null_stg_crashes_severity_code ......................... [RUN]
23:59:24  37 of 79 START test relationships_stg_casualties_crash_id__crash_id__ref_stg_crashes_  [RUN]
23:59:24  34 of 79 PASS not_null_stg_crashes_lga_name .................................... [PASS in 0.02s]
23:59:24  38 of 79 START test relationships_stg_crashes_release_id__release_id__source_lake_releases_  [RUN]
23:59:24  35 of 79 PASS not_null_stg_crashes_release_id .................................. [PASS in 0.03s]
23:59:24  36 of 79 PASS not_null_stg_crashes_severity_code ............................... [PASS in 0.03s]
23:59:24  37 of 79 PASS relationships_stg_casualties_crash_id__crash_id__ref_stg_crashes_  [PASS in 0.03s]
23:59:24  39 of 79 START test relationships_stg_crashes_severity_code__severity_code__ref_severity_levels_  [RUN]
23:59:24  40 of 79 START test relationships_stg_units_crash_id__crash_id__ref_stg_crashes_  [RUN]
23:59:24  41 of 79 START test unique_stg_crashes_crash_id ................................ [RUN]
23:59:24  38 of 79 PASS relationships_stg_crashes_release_id__release_id__source_lake_releases_  [PASS in 0.03s]
23:59:24  39 of 79 PASS relationships_stg_crashes_severity_code__severity_code__ref_severity_levels_  [PASS in 0.03s]
23:59:24  41 of 79 PASS unique_stg_crashes_crash_id ...................................... [PASS in 0.03s]
23:59:24  42 of 79 START sql table model main.fct_crashes ................................ [RUN]
23:59:24  40 of 79 PASS relationships_stg_units_crash_id__crash_id__ref_stg_crashes_ ..... [PASS in 0.05s]
23:59:25  42 of 79 OK created sql table model main.fct_crashes ........................... [OK in 0.52s]
23:59:25  43 of 79 START test accepted_values_fct_crashes_severity_code__False__1__2__3__4  [RUN]
23:59:25  44 of 79 START test accepted_values_fct_crashes_severity_name__Property_damage_only__Minor_injury__Serious_injury__Fatal  [RUN]
23:59:25  45 of 79 START test assert_casualty_rows_match_totals .......................... [RUN]
23:59:25  46 of 79 START test assert_fatal_casualties_match_total_fats ................... [RUN]
23:59:25  45 of 79 PASS assert_casualty_rows_match_totals ................................ [PASS in 0.02s]
23:59:25  43 of 79 PASS accepted_values_fct_crashes_severity_code__False__1__2__3__4 ..... [PASS in 0.02s]
23:59:25  46 of 79 PASS assert_fatal_casualties_match_total_fats ......................... [PASS in 0.02s]
23:59:25  44 of 79 PASS accepted_values_fct_crashes_severity_name__Property_damage_only__Minor_injury__Serious_injury__Fatal  [PASS in 0.02s]
23:59:25  47 of 79 START test non_negative_fct_crashes_casualty_rows ..................... [RUN]
23:59:25  48 of 79 START test non_negative_fct_crashes_total_fats ........................ [RUN]
23:59:25  49 of 79 START test not_null_fct_crashes_crash_id .............................. [RUN]
23:59:25  50 of 79 START test not_null_fct_crashes_pdo_regime_id ......................... [RUN]
23:59:25  47 of 79 PASS non_negative_fct_crashes_casualty_rows ........................... [PASS in 0.02s]
23:59:25  48 of 79 PASS non_negative_fct_crashes_total_fats .............................. [PASS in 0.02s]
23:59:25  49 of 79 PASS not_null_fct_crashes_crash_id .................................... [PASS in 0.02s]
23:59:25  50 of 79 PASS not_null_fct_crashes_pdo_regime_id ............................... [PASS in 0.02s]
23:59:25  51 of 79 START test not_null_fct_crashes_severity_code ......................... [RUN]
23:59:25  52 of 79 START test unique_fct_crashes_crash_id ................................ [RUN]
23:59:25  51 of 79 PASS not_null_fct_crashes_severity_code ............................... [PASS in 0.01s]
23:59:25  52 of 79 PASS unique_fct_crashes_crash_id ...................................... [PASS in 0.02s]
23:59:25  53 of 79 START sql table model main.dim_lga .................................... [RUN]
23:59:25  54 of 79 START sql table model main.fct_casualties ............................. [RUN]
23:59:25  55 of 79 START sql table model main.rpt_crash_type_severity .................... [RUN]
23:59:25  56 of 79 START sql table model main.rpt_monthly_severity ....................... [RUN]
23:59:25  53 of 79 OK created sql table model main.dim_lga ............................... [OK in 0.03s]
23:59:25  55 of 79 OK created sql table model main.rpt_crash_type_severity ............... [OK in 0.03s]
23:59:25  57 of 79 START sql table model main.rpt_region_fsi ............................. [RUN]
23:59:25  56 of 79 OK created sql table model main.rpt_monthly_severity .................. [OK in 0.03s]
23:59:25  58 of 79 START test accepted_values_dim_lga_main_stats_area__City__Metropolitan__Country  [RUN]
23:59:25  59 of 79 START test not_null_dim_lga_lga_name .................................. [RUN]
23:59:25  58 of 79 PASS accepted_values_dim_lga_main_stats_area__City__Metropolitan__Country  [PASS in 0.01s]
23:59:25  59 of 79 PASS not_null_dim_lga_lga_name ........................................ [PASS in 0.01s]
23:59:25  60 of 79 START test unique_dim_lga_lga_name .................................... [RUN]
23:59:25  61 of 79 START test non_negative_rpt_crash_type_severity_fsi_crashes ........... [RUN]
23:59:25  57 of 79 OK created sql table model main.rpt_region_fsi ........................ [OK in 0.03s]
23:59:25  62 of 79 START test not_null_rpt_crash_type_severity_crash_type ................ [RUN]
23:59:25  60 of 79 PASS unique_dim_lga_lga_name .......................................... [PASS in 0.02s]
23:59:25  61 of 79 PASS non_negative_rpt_crash_type_severity_fsi_crashes ................. [PASS in 0.02s]
23:59:25  63 of 79 START test unique_rpt_crash_type_severity_crash_type .................. [RUN]
23:59:25  64 of 79 START test non_negative_rpt_monthly_severity_fsi_crashes .............. [RUN]
23:59:25  62 of 79 PASS not_null_rpt_crash_type_severity_crash_type ...................... [PASS in 0.02s]
23:59:25  65 of 79 START test not_null_rpt_monthly_severity_crash_month .................. [RUN]
23:59:25  63 of 79 PASS unique_rpt_crash_type_severity_crash_type ........................ [PASS in 0.02s]
23:59:25  64 of 79 PASS non_negative_rpt_monthly_severity_fsi_crashes .................... [PASS in 0.02s]
23:59:25  66 of 79 START test unique_rpt_monthly_severity_crash_month .................... [RUN]
23:59:25  67 of 79 START test not_null_rpt_region_fsi_stats_area ......................... [RUN]
23:59:25  65 of 79 PASS not_null_rpt_monthly_severity_crash_month ........................ [PASS in 0.02s]
23:59:25  68 of 79 START test unique_rpt_region_fsi_stats_area ........................... [RUN]
23:59:25  66 of 79 PASS unique_rpt_monthly_severity_crash_month .......................... [PASS in 0.02s]
23:59:25  54 of 79 OK created sql table model main.fct_casualties ........................ [OK in 0.11s]
23:59:25  67 of 79 PASS not_null_rpt_region_fsi_stats_area ............................... [PASS in 0.02s]
23:59:25  69 of 79 START sql table model main.rpt_lga_fsi ................................ [RUN]
23:59:25  70 of 79 START sql table model main.rpt_kpis ................................... [RUN]
23:59:25  71 of 79 START test not_null_fct_casualties_crash_id ........................... [RUN]
23:59:25  68 of 79 PASS unique_rpt_region_fsi_stats_area ................................. [PASS in 0.02s]
23:59:25  72 of 79 START test relationships_fct_casualties_crash_id__crash_id__ref_fct_crashes_  [RUN]
23:59:25  71 of 79 PASS not_null_fct_casualties_crash_id ................................. [PASS in 0.02s]
23:59:25  70 of 79 OK created sql table model main.rpt_kpis .............................. [OK in 0.03s]
23:59:25  69 of 79 OK created sql table model main.rpt_lga_fsi ........................... [OK in 0.03s]
23:59:25  73 of 79 START test not_null_rpt_lga_fsi_lga_name .............................. [RUN]
23:59:25  74 of 79 START test unique_rpt_lga_fsi_lga_name ................................ [RUN]
23:59:25  72 of 79 PASS relationships_fct_casualties_crash_id__crash_id__ref_fct_crashes_  [PASS in 0.02s]
23:59:25  75 of 79 START sql table model main.rpt_annual_people .......................... [RUN]
23:59:25  73 of 79 PASS not_null_rpt_lga_fsi_lga_name .................................... [PASS in 0.01s]
23:59:25  74 of 79 PASS unique_rpt_lga_fsi_lga_name ...................................... [PASS in 0.01s]
23:59:25  75 of 79 OK created sql table model main.rpt_annual_people ..................... [OK in 0.11s]
23:59:25  76 of 79 START test non_negative_rpt_annual_people_admitted_to_hospital ........ [RUN]
23:59:25  77 of 79 START test non_negative_rpt_annual_people_fatalities .................. [RUN]
23:59:25  78 of 79 START test not_null_rpt_annual_people_crash_year ...................... [RUN]
23:59:25  79 of 79 START test unique_rpt_annual_people_crash_year ........................ [RUN]
23:59:25  77 of 79 PASS non_negative_rpt_annual_people_fatalities ........................ [PASS in 0.02s]
23:59:25  76 of 79 PASS non_negative_rpt_annual_people_admitted_to_hospital .............. [PASS in 0.02s]
23:59:25  78 of 79 PASS not_null_rpt_annual_people_crash_year ............................ [PASS in 0.02s]
23:59:25  79 of 79 PASS unique_rpt_annual_people_crash_year .............................. [PASS in 0.02s]
23:59:25  
23:59:25  Finished running 3 seeds, 9 table models, 63 data tests, 4 view models in 0 hours 0 minutes and 1.27 seconds (1.27s).
23:59:25  
23:59:25  Completed successfully
23:59:25  
23:59:25  Done. PASS=79 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=79
10:29:27.231 | INFO    | Task run 'dbt_build-070' - dbt build finished: pass=63, success=16
10:29:27.233 | INFO    | Task run 'dbt_build-070' - Finished in state Completed()
10:29:27.351 | INFO    | Task run 'benchmark_warehouse-ce5' - 
EXPLAIN ANALYZE (tile2_monthly_fsi_2021_2025, curated layout)
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││    Query Profiling Information    ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
explain analyze select crash_month, count(*) filter (where is_fsi) as fsi_crashes from read_parquet('/private/tmp/de-w7-build/original/project/data/lake/curated/fct_crashes/*/*.parquet', hive_partitioning=true) where crash_year between 2021 and 2025 group by crash_month order by crash_month
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 0.0015s             ││
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
│  /private/tmp/de-w7-build │
│   /original/project/data  │
│ /lake/curated/fct_crashes │
│  /crash_year=2021/part_0  │
│ .parquet, /private/tmp/de │
│ -w7-build/original/project│
│     /data/lake/curated    │
│  /fct_crashes/crash_year  │
│   =2022/part_0.parquet,   │
│  /private/tmp/de-w7-build │
│   /original/project/data  │
│ /lake/curated/fct_crashes │
│  /crash_year=2023/part_0  │
│ .parquet, /private/tmp/de │
│ -w7-build/original/project│
│     /data/lake/curated    │
│  /fct_crashes/crash_year  │
│   =2024/part_0.parquet,   │
│  /private/tmp/de-w7-build │
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
10:29:27.370 | INFO    | Task run 'benchmark_warehouse-ce5' - 
EXPLAIN ANALYZE (tile1_crash_type_fsi_2024, curated layout)
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││    Query Profiling Information    ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
explain analyze select crash_type, count(*) as fsi_crashes from read_parquet('/private/tmp/de-w7-build/original/project/data/lake/curated/fct_crashes/*/*.parquet', hive_partitioning=true) where crash_year = 2024 and severity_code >= 3 group by crash_type order by crash_type
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
│  /private/tmp/de-w7-build │
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
10:29:27.391 | INFO    | Task run 'benchmark_warehouse-ce5' - 
Partitioning and clustering benchmark (same rows, 8,192-row row groups)
10:29:27.391 | INFO    | Task run 'benchmark_warehouse-ce5' - query                              layout       files   row groups     rows to read  median ms
10:29:27.391 | INFO    | Task run 'benchmark_warehouse-ce5' - ----------------------------------------------------------------------------------------------
10:29:27.391 | INFO    | Task run 'benchmark_warehouse-ce5' - tile2_monthly_fsi_2021_2025        flat           1/1        10/26     73788/204860       1.36
10:29:27.391 | INFO    | Task run 'benchmark_warehouse-ce5' - tile2_monthly_fsi_2021_2025        curated       5/14        10/31     65655/204860       1.11
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' -                                    same result on both layouts: True
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' - tile1_crash_type_fsi_2024          flat           1/1         3/26     24576/204860       1.16
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' - tile1_crash_type_fsi_2024          curated       1/14         2/31     13140/204860       0.79
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' -                                    same result on both layouts: True
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' - lga_drilldown_adelaide_q1_2024     flat           1/1         2/26     16384/204860       0.99
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' - lga_drilldown_adelaide_q1_2024     curated      14/14         1/31      8192/204860       1.14
10:29:27.392 | INFO    | Task run 'benchmark_warehouse-ce5' -                                    same result on both layouts: True
10:29:27.393 | INFO    | Task run 'benchmark_warehouse-ce5' - 
benchmark written to /private/tmp/de-w7-build/original/project/data/warehouse/benchmark.json
10:29:27.393 | INFO    | Task run 'benchmark_warehouse-ce5' - Finished in state Completed()
10:29:27.407 | INFO    | Task run 'export_dashboard-c73' - exported 168 months, 13 crash types; crashes=204860 fsi_crashes=10204 fatalities=1337 serious_injuries=10435
10:29:27.407 | INFO    | Task run 'export_dashboard-c73' - 
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
Monthly FSI: peak month 2024-03 (96); 12-month mean lowest 46.17 (to 2018-10), highest 73.25 (to 2024-08)
10:29:27.407 | INFO    | Task run 'export_dashboard-c73' - dashboard JSON written to /private/tmp/de-w7-build/web/app/project/dashboard-data.json (69590 bytes)
10:29:27.408 | INFO    | Task run 'export_dashboard-c73' - Finished in state Completed()
10:29:27.471 | INFO    | Flow run 'jade-crab' - Finished in state Completed()
10:29:27.479 | INFO    | prefect - Stopping temporary server on http://127.0.0.1:8743
/Applications/Xcode.app/Contents/Developer/usr/bin/make test
.venv/bin/python -m pytest -m "not integration" -v
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.1.1, pluggy-1.7.0 -- /private/tmp/de-w7-build/original/project/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/tmp/de-w7-build/original/project
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collecting ... collected 43 items / 17 deselected / 26 selected

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

====================== 26 passed, 17 deselected in 8.84s =======================
.venv/bin/python -m pytest -m integration -v
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.1.1, pluggy-1.7.0 -- /private/tmp/de-w7-build/original/project/.venv/bin/python
cachedir: .pytest_cache
rootdir: /private/tmp/de-w7-build/original/project
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collecting ... collected 43 items / 26 deselected / 17 selected

tests/test_dashboard_export.py::test_dashboard_has_at_least_two_tiles PASSED [  5%]
tests/test_dashboard_export.py::test_months_are_continuous_from_2012_to_2025 PASSED [ 11%]
tests/test_dashboard_export.py::test_rolling_mean_is_the_trailing_twelve_month_average PASSED [ 17%]
tests/test_dashboard_export.py::test_totals_reconcile_with_the_warehouse PASSED [ 23%]
tests/test_dashboard_export.py::test_crash_types_are_sorted_by_fsi PASSED [ 29%]
tests/test_dashboard_export.py::test_only_the_latest_year_is_provisional PASSED [ 35%]
tests/test_dashboard_export.py::test_export_is_deterministic_and_matches_the_committed_file PASSED [ 41%]
tests/test_dashboard_export.py::test_attribution_and_release_dates_travel_with_the_data PASSED [ 47%]
tests/test_dashboard_export.py::test_2023_matches_the_published_road_safety_annual_report PASSED [ 52%]
tests/test_warehouse.py::test_lake_has_one_partition_per_year_for_every_table PASSED [ 58%]
tests/test_warehouse.py::test_row_counts_carry_through_from_lake_to_warehouse PASSED [ 64%]
tests/test_warehouse.py::test_lake_counts_match_the_crash_totals PASSED  [ 70%]
tests/test_warehouse.py::test_fct_crashes_is_stored_in_cluster_order PASSED [ 76%]
tests/test_warehouse.py::test_curated_export_is_partitioned_with_small_sorted_row_groups PASSED [ 82%]
tests/test_warehouse.py::test_every_dbt_node_passed PASSED               [ 88%]
tests/test_warehouse.py::test_benchmark_shows_less_data_to_read_on_the_curated_layout PASSED [ 94%]
tests/test_warehouse.py::test_lga_aliases_leave_no_trailing_full_stops PASSED [100%]

====================== 17 passed, 26 deselected in 1.49s =======================
make all finished in 37s
$ du -sh data/landing data/lake/raw data/lake/curated data/warehouse/sa_crash.duckdb
 16M	data/landing
8.9M	data/lake/raw
4.3M	data/lake/curated
 12M	data/warehouse/sa_crash.duckdb
```
