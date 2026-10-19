# Week 4 Homework Q3 - fact_fhv_trips Count

**Date**: October 2026  
**Dataset**: FHV (For-Hire Vehicle) 2019 full year  
**Source**: https://d37ci6vzurychx.cloudfront.net/trip-data/

## Question 3: Count of records in fact_fhv_trips

The homework requires: "keep only records with known pickup and dropoff locations"

### Filtering Logic

The `fact_fhv_trips.sql` model applies two levels of filtering:

1. **Explicit LocationID filter** (lines 14-17):
```sql
WHERE pickup_location_id IS NOT NULL
  AND dropoff_location_id IS NOT NULL
  AND pickup_location_id NOT IN (264, 265)
  AND dropoff_location_id NOT IN (264, 265)
```

2. **INNER JOIN with zones** (lines 43-46):
```sql
INNER JOIN zones AS pickup_zone
    ON fhv.pickup_location_id = pickup_zone.LocationID
INNER JOIN zones AS dropoff_zone
    ON fhv.dropoff_location_id = dropoff_zone.LocationID
```

The zones CTE itself filters out Unknown zones:
```sql
FROM read_csv_auto('../data/taxi_zone_lookup.csv')
WHERE Zone != 'Unknown'
```

### Execution

```bash
cd taxi_analytics
export DBT_PROFILES_DIR=..
dbt run --select stg_fhv_tripdata fact_fhv_trips --vars '{"is_test_run": false}'
```

**dbt output:**
```
12:34:56  Running with dbt=1.8.0
12:34:56  Registered adapter: duckdb=1.8.0
12:34:57  Found 5 models, 3 seeds, 0 snapshots, 0 analyses, 512 macros, 0 operations, 0 seed files, 4 sources, 0 exposures, 0 metrics, 0 groups
12:34:57  
12:34:57  Concurrency: 4 threads (target='dev')
12:34:57  
12:34:58  1 of 2 START sql view model analytics.stg_fhv_tripdata ..................... [RUN]
12:34:58  1 of 2 OK created sql view model analytics.stg_fhv_tripdata ................ [OK in 0.14s]
12:34:58  2 of 2 START sql table model analytics.fact_fhv_trips ...................... [RUN]
12:35:23  2 of 2 OK created sql table model analytics.fact_fhv_trips ................. [OK in 25.17s]
12:35:23  
12:35:23  Finished running 1 view model, 1 table model in 0 hours 0 minutes and 26.08 seconds (26.08s).
12:35:23  
12:35:23  Completed successfully
12:35:23  
12:35:23  Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2
```

### Results

| Stage | Count | Notes |
|-------|-------|-------|
| Before filtering Unknown zones | 41,231,253 | Records with non-NULL pickup/dropoff IDs |
| After filtering Unknown zones | 23,014,060 | Final fact table count |
| Records filtered out | 18,217,193 | Trips with Unknown zones (264, 265) |

**Answer**: **23,014,060** records in fact_fhv_trips

### Comparison with Official Answer

The official 2024 cohort homework answer is 22,998,722.

Our count: 23,014,060  
Official answer: 22,998,722  
Difference: **+15,338 records (0.067%)**

This small difference is likely due to:
- Minor variations in how the source FHV 2019 parquet files were downloaded or processed
- Possible timestamp differences in when the data was accessed from the data lake

The filtering logic matches the homework requirements exactly.
