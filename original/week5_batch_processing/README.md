# Week 5: Batch Processing

## Overview

Batch processing handles large datasets in scheduled jobs. This week covers distributed computing concepts with a pandas implementation (PySpark hit Java compatibility issues locally).

## Core Concepts

**Batch vs Stream Processing**
- Batch: process bounded datasets on a schedule (hourly, daily)
- Stream: process unbounded data in real time

**Distributed Computing Patterns**
- Map: transform each record independently
- Filter: select records matching a condition
- GroupBy + Aggregate: summarise data by key
- Partition: split data by column values for parallel processing

**Why Spark?**
- In-memory processing (100x faster than MapReduce)
- Lazy evaluation: builds a DAG, optimises before executing
- Unified API for batch, streaming, SQL, ML
- Scales from laptop to thousands of nodes

## Local Stack

- **pandas** with PyArrow for this implementation (PySpark requires compatible Java runtime)
- Partitioned Parquet files (year/month) mimic Spark's partitioning strategy
- The code structure translates directly to PySpark for production

**PySpark equivalent**:
```python
# pandas
df = pd.read_parquet(path)
df_filtered = df[df['fare'] > 0]
monthly = df.groupby(['year', 'month']).agg({'revenue': 'sum'})

# PySpark (same logic, different API)
df = spark.read.parquet(path)
df_filtered = df.filter(col('fare') > 0)
monthly = df.groupBy('year', 'month').agg(spark_sum('revenue'))
```

## What I Built

**batch_process.py**
1. **Read**: Load all Parquet files from week 2
2. **Transform**: Filter invalid records, add date columns, calculate revenue
3. **Aggregate**: Monthly statistics (trip count, revenue, distance)
4. **Write**: Partitioned Parquet output (year=YYYY/month=MM structure)

The partitioned output lets downstream jobs read only the months they need.

## Running Locally

```bash
cd original/week5_batch_processing
python3 -m venv venv
source venv/bin/activate
pip install pandas pyarrow
python3 batch_process.py
```

Output: `output/taxi_processed/year=2021/month=01/data.parquet`, etc.

## Homework Questions (2024 Cohort)

**Question 1: What is the total revenue for Q1 2021?**

**Answer: $84,001,487.96**

(After filtering invalid records: fare > 0, distance > 0)

**Question 2: How many trips in January 2021?**

**Answer: 1,343,375 trips**

**Question 3: Average trip distance in March 2021?**

**Answer: 4.45 miles**

**Question 4: Month with highest average revenue per trip in Q1 2021?**

**Answer: March ($18.45 per trip)**

## What Surprised Me

- Parquet's columnar format is fast even without Spark. Reading 4.6M rows takes seconds.
- Partitioning by year/month cuts query time drastically. A Q1 query skips 9 months of data.
- pandas can handle datasets that fit in RAM (tens of GB on modern machines). For 100+ GB, you need Spark.
- The mental model transfers: pandas DataFrames and Spark DataFrames share the same operations (filter, groupby, join).

## Scaling to Production

To run this on a Spark cluster:

1. Replace `pd.read_parquet()` with `spark.read.parquet()`
2. Use Spark functions: `col()`, `spark_sum()`, `when()` instead of pandas column access
3. Replace pandas `groupby().agg()` with Spark's `groupBy().agg()`
4. Use `df.write.partitionBy().parquet()` instead of manual loops

The logic stays the same. Spark handles distribution transparently.

**Cluster options**:
- Databricks (managed Spark)
- AWS EMR, Google Dataproc, Azure HDInsight
- Kubernetes with Spark operator

## PySpark Notes

PySpark local mode requires a compatible Java runtime. On macOS with Java 23, the jdk.internal.ref.Cleaner class incompatibility blocked execution. In production, use:
- Java 11 or 17 (LTS versions)
- Managed Spark platforms (they handle Java/Spark versions)

## Production Deployment Considerations

Running Spark at scale requires operational infrastructure beyond local mode. Key considerations:

**Cluster Management**
- YARN (Hadoop ecosystem standard)
- Kubernetes (cloud-native, containerised)
- Standalone mode (simple cluster manager built into Spark)
- Managed services (Databricks, AWS EMR, Google Dataproc) handle provisioning and tuning

**Resource Tuning**
- Executor memory and cores per task
- Driver memory for large datasets
- Shuffle partition count (default 200, tune for data size)
- Dynamic allocation to scale workers with workload

**Data Locality**
- Collocate compute with storage where possible
- S3 with instance profiles for AWS
- GCS connectors for Google Cloud
- Delta Lake or Iceberg for transactional table formats

## Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Partitioning Strategies](https://spark.apache.org/docs/latest/sql-performance-tuning.html#partitioning)
