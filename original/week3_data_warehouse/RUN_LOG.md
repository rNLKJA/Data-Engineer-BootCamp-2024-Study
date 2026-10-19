================================================================================
Week 3: Data Warehouse Queries with DuckDB
================================================================================

[Q1] Row count for January 2021:
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│      1369769 │
└──────────────┘

[Q2] Total trip distance for Q1 2021 (Jan, Feb, Mar):
┌────────────────────┐
│ total_trip_dist_q1 │
│       double       │
├────────────────────┤
│       2.0658914e07 │
└────────────────────┘
     20,658,913.80 miles

[Q6a] Full scan EXPLAIN (all partitions):
     ┌───────────────────────────┐
│    UNGROUPED_AGGREGATE    │
│    ────────────────────   │
│        Aggregates:        │
│        count_star()       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│        READ_PARQUET       │
│    ────────────────────   │
│         Function:         │
│        READ_PARQUET       │
│                           │
│      ~4,751,493 rows      │
└───────────────────────────┘


[Q6b] Partitioned query EXPLAIN (only Jan 2021):
     ┌───────────────────────────┐
│      COLUMN_DATA_SCAN     │
│    ────────────────────   │
│           ~1 row          │
└───────────────────────────┘


[Bonus] Top 5 pickup locations in Q1 2021:
┌────────────────────┬──────────────┐
│ PULocationID       │ trip_count   │
│      int64         │    int64     │
├────────────────────┼──────────────┤
│                236 │       248310 │
│                237 │       247818 │
│                141 │       155513 │
│                239 │       152012 │
│                161 │       151680 │
└────────────────────┴──────────────┘

[Bonus] Row count per partition (month):
┌─────────────┬──────────────┐
│ pickup_month│ count_star() │
│    int64    │    int64     │
├─────────────┼──────────────┤
│           1 │      1369769 │
│           2 │      1371709 │
│           3 │      1925152 │
└─────────────┴──────────────┘

================================================================================
All queries complete!
================================================================================

## Week 3 Homework - Green Taxi 2022

**Date**: October 2026
**Dataset**: Green taxi 2022 (all 12 months)
**Source**: https://d37ci6vzurychx.cloudfront.net/trip-data/

### Execution

```bash
python homework_green_2022.py
```

### Results

**Question 1**: 840,402 records
**Question 2**: 0 MB External / 6.41 MB Materialized (BigQuery context, not reproducible locally)
**Question 3**: 1,622 records with fare_amount = 0
**Question 4**: Partition by lpep_pickup_datetime, Cluster on PULocationID
**Question 5**: 12.82 MB non-partitioned / 1.12 MB partitioned (BigQuery context, not reproducible locally)
**Question 6**: GCP Bucket
**Question 7**: False
**Question 8**: COUNT(*) uses metadata only, ~0 MB scanned
