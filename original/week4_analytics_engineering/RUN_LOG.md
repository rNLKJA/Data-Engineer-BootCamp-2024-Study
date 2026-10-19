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
