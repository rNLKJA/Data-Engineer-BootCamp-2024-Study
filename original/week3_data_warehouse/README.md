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

**Official 2024 Cohort Homework**: [Module 3 Homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/03-data-warehouse/homework.md)

Dataset: Green taxi 2022 parquet files

Note: The official homework uses BigQuery. This implementation uses DuckDB as a local substitute. BigQuery-specific questions (like bytes scanned estimates) note where behaviour differs.

### Question 1: Count of records for the 2022 Green Taxi Data

**Query:**
```python
python homework_green_2022.py
```

**Answer:** 840,402 records

### Question 2: Distinct PULocationIDs - estimated data read

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the external table and the materialized table.

**DuckDB Note:** DuckDB doesn't show "estimated bytes to scan" like BigQuery. In BigQuery:
- External table: reads data from GCS, scans actual parquet files
- Materialized table: reads from BigQuery's internal storage

**Answer (from BigQuery context):** 0 MB for External Table, 6.41 MB for Materialized Table

(not reproducible locally with DuckDB's query execution model)

### Question 3: Records with fare_amount of 0

**Query:**
```sql
SELECT COUNT(*) FROM green_taxi_materialized WHERE fare_amount = 0
```

**Answer:** 1,622 records

### Question 4: Best strategy for optimized table

What is the best strategy to make an optimized table in BigQuery if your query will always order the results by PULocationID and filter based on lpep_pickup_datetime?

**Answer:** Partition by lpep_pickup_datetime, Cluster on PULocationID

Rationale: Partition by the filter column (datetime) for coarse pruning, cluster by the order-by column (location) for fine-grained sorting within partitions.

### Question 5: Query bytes for distinct PULocationID in June 2022

Write a query to retrieve distinct PULocationID between 2022-06-01 and 2022-06-30 (inclusive). Compare bytes scanned between non-partitioned and partitioned tables.

**DuckDB Note:** DuckDB's local execution doesn't show "bytes to scan" estimates like BigQuery.

**Answer (from BigQuery context):** 12.82 MB for non-partitioned table, 1.12 MB for partitioned table

(not reproducible locally with DuckDB)

### Question 6: Where is data stored in External Table?

**Answer:** GCP Bucket

External tables in BigQuery point to data stored in GCS buckets, not in BigQuery's internal storage.

### Question 7: Is it best practice to always cluster data?

**Answer:** False

Clustering is beneficial for:
- Large tables (> 1 GB)
- High-cardinality columns
- Columns frequently used in filters or GROUP BY

For small tables or low-cardinality columns, clustering overhead outweighs performance gains.

---

_Completed October 2026 as part of the Data Engineering Zoomcamp 2024 study with Claude as a pair programmer._
