================================================================================
Week 3: Data Warehouse Queries with DuckDB
================================================================================

[Q1] Row count for January 2021:
     1,369,769 rows

[Q2] Total trip distance for Q1 2021 (Jan, Feb, Mar):
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
     Location 236: 248,310 trips
     Location 237: 247,818 trips
     Location 141: 155,513 trips
     Location 239: 152,012 trips
     Location 161: 151,680 trips

[Bonus] Row count per partition (month):
     Month 01: 1,369,769 rows
     Month 02: 1,371,709 rows
     Month 03: 1,925,152 rows

================================================================================
All queries complete!
================================================================================
