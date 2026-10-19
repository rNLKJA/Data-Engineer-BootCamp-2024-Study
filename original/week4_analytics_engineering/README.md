# Week 4: Analytics Engineering with dbt

## Overview

Analytics engineering sits between data engineering and analytics. This week explores dbt (data build tool) with dbt-duckdb as a local substitute for dbt-bigquery.

## Core Concepts

**dbt (data build tool)**
- SQL-based transformation tool for the modern data stack
- Version control for analytics code
- Testing and documentation built in
- Modular, reusable SQL with Jinja templating
- Materialisation strategies: views, tables, incremental

**Layered Architecture**
- Staging: light transformations, renaming, type casting
- Intermediate: business logic, joins
- Marts: final models for consumption (fact/dimension tables, aggregations)

**Local Stack Differences**
- BigQuery → DuckDB (analytical SQL engine, embedded)
- GCS → local Parquet files from week 2
- BigQuery's native partitioning/clustering → DuckDB EXPLAIN for query planning, partitioned Parquet on disk

## Project Structure

```
taxi_analytics/
├── dbt_project.yml          # Project configuration
├── models/
│   ├── stg_yellow_trips.sql  # Staging: raw data with light cleaning
│   ├── fact_trips.sql        # Fact table with revenue calculations
│   ├── monthly_revenue.sql   # Aggregate monthly metrics
│   └── schema.yml            # Tests and documentation
```

## What I Built

### Models

**stg_yellow_trips** (view)
Reads Q1 2021 yellow taxi Parquet files from week 2, constructs a trip_id, and does light type casting. DuckDB's `read_parquet()` handles the glob pattern directly.

**fact_trips** (table)
Adds calculated fields: revenue (fare + extras + tolls + tips + surcharges), date parts for analysis. This is the core analytical table.

**monthly_revenue** (table)
Aggregates by month: total trips, total/avg revenue, total/avg distance, avg passengers. Clean rollup for time-series analysis.

### Tests

dbt's built-in tests verify data quality:
- `not_null` on primary keys
- Column-level tests defined in `schema.yml`

Run with `dbt test`.

## Running Locally

**Setup**
```bash
cd original/week4_analytics_engineering
python3 -m venv venv
source venv/bin/activate
pip install dbt-core dbt-duckdb
```

**Run models**
```bash
cd taxi_analytics
export DBT_PROFILES_DIR=..
dbt run
dbt test
```

The database file `taxi.duckdb` is created in the project directory.

## Homework Questions (2024 Cohort)

**Question 1: What is the total revenue for Q1 2021 (Jan-Mar)?**

Query:
```sql
SELECT SUM(revenue) AS total_revenue
FROM analytics.fact_trips
WHERE pickup_year = 2021 AND pickup_month_num BETWEEN 1 AND 3;
```

**Answer: $74,191,439.46**

(Computed from monthly_revenue: $21,567,312.70 + $21,794,089.30 + $30,830,037.46)

**Question 2: How many trips in January 2021?**

Query:
```sql
SELECT COUNT(*) AS trip_count
FROM analytics.fact_trips
WHERE pickup_year = 2021 AND pickup_month_num = 1;
```

**Answer: 1,343,375 trips**

**Question 3: Average trip distance in March 2021?**

Query:
```sql
SELECT AVG(trip_distance) AS avg_distance
FROM analytics.fact_trips
WHERE pickup_year = 2021 AND pickup_month_num = 3;
```

**Answer: 4.45 miles**

**Question 4: Month with highest average revenue per trip?**

Query:
```sql
SELECT pickup_month, avg_revenue_per_trip
FROM analytics.monthly_revenue
WHERE pickup_year = 2021
ORDER BY avg_revenue_per_trip DESC
LIMIT 1;
```

**Answer: February 2021 ($16.19 per trip)**

## What Surprised Me

- DuckDB's `read_parquet()` with glob patterns means no ETL into the database first—just query the files directly.
- dbt's ref() macro builds the DAG automatically. Change the materialisation, and dbt handles the dependency order.
- The generated documentation is actually useful. `dbt docs generate && dbt docs serve` gives you a full data catalogue with lineage.
- Tests run fast. A few hundred lines of YAML give you continuous data quality checks.

## BigQuery vs DuckDB

| Feature | BigQuery | DuckDB (this project) |
|---------|----------|------------------------|
| Storage | Columnar, serverless | In-process, Parquet or in-DB |
| Partitioning | Native table partitioning by date/int | Partitioned Parquet files on disk |
| Clustering | Native clustering within partitions | Query planner optimises (check with EXPLAIN) |
| Cost model | Pay per TB scanned | Free, local |
| Scale | Petabytes | Fits in memory or disk |

**Partitioning equivalent**: Instead of `PARTITION BY DATE(pickup_datetime)` in BigQuery DDL, I store Parquet files in `2021/01/`, `2021/02/` structure. DuckDB's Hive partitioning support reads only the files needed when you filter on year/month.

**Clustering equivalent**: DuckDB's query planner and statistics on Parquet files handle this. Use `EXPLAIN` to see the plan.

## Next Steps

- Incremental models for large datasets (append-only or merge)
- Snapshots for slowly changing dimensions
- Exposures to link dbt models to BI dashboards
- dbt Cloud for scheduling (or Prefect, Dagster orchestrating dbt CLI)

## Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt-duckdb adapter](https://github.com/duckdb/dbt-duckdb)
- [DuckDB SQL Reference](https://duckdb.org/docs/sql/introduction)
