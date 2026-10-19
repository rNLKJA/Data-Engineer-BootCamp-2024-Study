# Week 3 — Data Warehouse

> Part of my [Data Engineering Zoomcamp 2024 study repo](../../README.md). These are my notes on data warehousing with DuckDB (local substitute for BigQuery), covering partitioning, clustering, and query optimization.

## What is a Data Warehouse?

A data warehouse is a centralised repository optimised for analytical queries, not transactional operations. Unlike OLTP databases (Postgres, MySQL) that handle many small read/write operations, OLAP warehouses (BigQuery, Snowflake, Redshift) excel at scanning large datasets for aggregations and analytics.

Key characteristics:
- **Column-oriented storage**: reading specific columns is fast without scanning entire rows
- **Partitioning**: data split by date/category for faster query pruning
- **Clustering**: rows with similar values grouped together within partitions
- **Compression**: columnar data compresses extremely well
- **Separation of storage and compute**: scale query power independently of data size

Common use cases: business intelligence, reporting dashboards, ML feature stores, historical analysis.

## Why DuckDB?

This week uses **DuckDB** instead of BigQuery. DuckDB is an embedded analytical database (like SQLite but for analytics) that runs entirely locally with no cloud account. It reads parquet directly, supports partitioned queries, and has BigQuery-compatible SQL.

Differences from BigQuery:
- **Local**: no cloud costs, no account needed, data stays on disk
- **Embedded**: runs in-process, no server to manage
- **Partitioning**: manual via file structure (`data_lake/yellow_taxi/year=2021/month=01/`), not built-in table metadata
- **Clustering**: simulated with sorted parquet writes
- **Query planner**: `EXPLAIN` shows execution plans similar to BigQuery's query execution graph

The concepts (partitioning, clustering, query optimization) translate directly to BigQuery.

## Partitioning and Clustering

**Partitioning** divides a table into chunks by a column (usually date). Queries filtering on the partition key skip irrelevant chunks. Example: partitioning taxi trips by pickup date means a query for January 2021 only scans that month's files, not the full dataset.

In DuckDB with parquet files:
- Partition structure: `year=2021/month=01/` directories (Hive-style partitioning)
- DuckDB reads this automatically with `read_parquet('data_lake/**/*.parquet', hive_partitioning=1)`
- Queries with `WHERE year = 2021 AND month = 1` prune to that partition

**Clustering** sorts rows within a partition by frequently-filtered columns. Parquet's row groups benefit: a query filtering on `PULocationID` can skip row groups where `PULocationID` is outside the filter range (min/max statistics).

In DuckDB:
- Write parquet sorted by clustering columns: `COPY (SELECT * FROM table ORDER BY PULocationID) TO 'file.parquet'`
- Parquet stores min/max stats per row group, enabling pruning

The combination: partition by date (coarse pruning), cluster by location or vendor (fine pruning within partitions).

## BigQuery Concepts vs DuckDB

| BigQuery Concept       | DuckDB Equivalent                                  | Notes                                                      |
| ---------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| Partitioned table      | Hive-partitioned parquet directory structure       | `year=X/month=Y/` directories                              |
| Clustering             | Sorted parquet writes                              | `ORDER BY` before writing parquet                          |
| Query execution graph  | `EXPLAIN` output                                   | Shows filters, scans, projections                          |
| Slots / parallel scans | DuckDB parallel parquet reader                     | Automatic, configurable via `threads` setting              |
| On-demand pricing      | Free (local compute)                               | No cost, but limited to local machine resources            |
| Storage pricing        | Disk space                                         | Parquet is highly compressed                               |
| Query caching          | Manual (save query results to parquet)             | No automatic result caching                                |
| INFORMATION_SCHEMA     | `duckdb_tables()`, `duckdb_columns()` system views | Introspection available                                    |
| ML (BQML)              | Not available in DuckDB                            | Use Python (scikit-learn, pandas) or external tools        |
| Streaming inserts      | Append new parquet files to partitions             | No real-time streaming, batch-oriented                     |
| Time-travel            | Not available                                      | Would require manual versioned parquet snapshots           |
| External tables        | `read_parquet('s3://...')` or local paths          | Can read from S3, GCS (with extensions), HTTP, local files |

## What Surprised Me

**DuckDB's parquet performance**: querying partitioned parquet is instant even on millions of rows. The combination of columnar format, compression, and partition pruning makes analytical queries feel interactive on a laptop.

**Hive partitioning is automatic**: DuckDB detects `year=X/month=Y/` directory structures without config. Just point it at the root and filter normally, it prunes partitions automatically.

**EXPLAIN is detailed**: the query plan shows exactly which files and row groups were scanned, making it easy to verify that partition and clustering pruning worked.

**No indexes needed**: unlike Postgres where you index columns for fast lookups, columnar parquet + partition pruning handles analytical queries without traditional indexes.

## Running Queries

Install DuckDB:
```bash
cd original/week3_data_warehouse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the example queries:
```bash
python queries.py
```

Or use the DuckDB CLI:
```bash
duckdb
```

Load data and query:
```sql
-- Load all partitions
CREATE VIEW taxi AS 
SELECT * FROM read_parquet('../week2_workflow_orchestration/data_lake/yellow_taxi/**/*.parquet', hive_partitioning=1);

-- Query with partition pruning
SELECT COUNT(*) FROM taxi WHERE year = 2021 AND month = 1;

-- Check execution plan
EXPLAIN SELECT COUNT(*) FROM taxi WHERE year = 2021 AND month = 1;
```

## Homework

### Question 1: Row count for January 2021

**Query:**
```sql
SELECT COUNT(*) FROM read_parquet('../week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/*.parquet');
```

**Answer:** 1,369,769 rows

### Question 2: Total trip distance for Q1 2021

**Query:**
```sql
SELECT SUM(trip_distance) AS total_distance
FROM read_parquet('../week2_workflow_orchestration/data_lake/yellow_taxi/2021/*/*.parquet', hive_partitioning=1)
WHERE year = 2021 AND month IN (1, 2, 3);
```

**Answer:** 16,276,016.61 miles

### Question 3: What is partitioning?

Partitioning splits a table into smaller chunks based on a column value (usually a date). Each partition is stored separately. Queries filtering on the partition key only scan relevant partitions, skipping the rest. This reduces query cost and latency.

Example: a table partitioned by `pickup_date` stores each day's data in separate files. A query for January 1st scans only that day's partition, not the full year.

Benefits:
- **Faster queries**: less data scanned
- **Lower cost**: cloud warehouses charge per byte scanned
- **Easier management**: drop old partitions without rewriting the whole table

### Question 4: What is clustering?

Clustering sorts rows within a partition by one or more columns. Rows with similar values are stored together. Columnar formats like parquet maintain min/max statistics per row group, allowing queries to skip row groups where the filter can't match.

Example: cluster taxi data by `PULocationID`. A query filtering on `PULocationID = 50` only reads row groups containing location 50, skipping the rest.

Clustering complements partitioning: partition by date (coarse pruning), cluster by frequently-filtered columns like location or vendor (fine pruning).

### Question 5: How does DuckDB's partition pruning work?

DuckDB supports Hive-style partitioning: directory names encode partition keys (`year=2021/month=01/`). When reading with `hive_partitioning=1`, DuckDB:
1. Scans the directory structure to discover partitions
2. Parses partition keys from directory names
3. Evaluates filters in the `WHERE` clause against partition keys
4. Skips partitions that can't match the filter

Example:
```sql
SELECT * FROM read_parquet('data_lake/**/*.parquet', hive_partitioning=1)
WHERE year = 2021 AND month = 1;
```

DuckDB only reads files under `year=2021/month=01/`, ignoring all other months. The `EXPLAIN` output confirms which partitions were scanned.

### Question 6: Compare a full-scan query to a partitioned query

**Full scan (no partition filter):**
```sql
EXPLAIN SELECT COUNT(*) FROM read_parquet('../week2_workflow_orchestration/data_lake/**/*.parquet', hive_partitioning=1);
```

This scans all parquet files in all partitions.

**Partitioned query:**
```sql
EXPLAIN SELECT COUNT(*) FROM read_parquet('../week2_workflow_orchestration/data_lake/**/*.parquet', hive_partitioning=1)
WHERE year = 2021 AND month = 1;
```

This scans only the January 2021 partition. The `EXPLAIN` output shows fewer files scanned. On a dataset spanning years, the partitioned query is orders of magnitude faster.

**Observation**: partition pruning works even without explicitly creating a table. DuckDB's Hive partitioning support makes it transparent.

---

_Completed October 2026 as part of the Data Engineering Zoomcamp 2024 study with Claude as a pair programmer._
