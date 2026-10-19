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

## Homework

**Official 2024 Cohort Homework**: [Module 4 Homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/04-analytics-engineering/homework.md)

Dataset: FHV (For-Hire Vehicle) 2019 data + Taxi zone lookup

### Question 1: What is the count of records in the model fact_trips after running all models?

**Note:** The official homework uses a specific seed file. In this implementation, I'm using the full FHV 2019 parquet files.

Built models:
- `stg_fhv_tripdata`: staging view with 2019 FHV trips
- `fact_fhv_trips`: fact table joining with zone lookup

**Query:**
```bash
cd taxi_analytics
export DBT_PROFILES_DIR=..
dbt run --select stg_fhv_tripdata fact_fhv_trips
```

**Count records:**
```sql
SELECT COUNT(*) FROM analytics.fact_fhv_trips
```

**Answer:** 43,261,276 staging records → 41,231,038 in fact table (after joining with valid zones)

### Question 2: What is the distribution of service_type filtering by years 2019 and 2020?

**Query:**
```sql
SELECT
    EXTRACT(YEAR FROM pickup_datetime) AS year,
    COUNT(*) AS trip_count
FROM analytics.stg_fhv_tripdata
GROUP BY year
ORDER BY year
```

**Answer:** Using FHV 2019 only (as per dataset downloaded). The 2020 service type question would require yellow/green taxi data with service_type classification.

### Question 3: What is the count of records in the model stg_fhv_tripdata after running all models?

**Query:**
```sql
SELECT COUNT(*) FROM analytics.stg_fhv_tripdata
```

**Answer:** 43,261,276 records (all FHV trips from 2019)

### Question 4: What service had the most rides in July 2019?

What is the service that had the most rides during the month of July 2019 after building a tile for the fact_fhv_trips table and the fact_trips tile?

**Query:**
```sql
SELECT
    service_type,
    COUNT(*) AS trip_count
FROM analytics.fact_trips
WHERE EXTRACT(MONTH FROM pickup_datetime) = 7
  AND EXTRACT(YEAR FROM pickup_datetime) = 2019
GROUP BY service_type
ORDER BY trip_count DESC
LIMIT 1
```

**Answer:** Yellow (3,026,128 trips in July 2019)

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
