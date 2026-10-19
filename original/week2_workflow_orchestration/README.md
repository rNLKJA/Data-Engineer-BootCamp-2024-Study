# Week 2 — Workflow Orchestration

> Part of my [Data Engineering Zoomcamp 2024 study repo](../../README.md). These are my notes on workflow orchestration with Prefect, building an ETL pipeline that downloads NYC taxi data and loads it into a data lake (local filesystem, standing in for GCS).

## What is Workflow Orchestration?

Workflow orchestration automates the sequencing, monitoring and error handling of data pipeline tasks. Instead of manually running scripts in order or writing fragile cron jobs, an orchestrator like Prefect or Dagster defines tasks as code, tracks their state, handles retries and alerts you when something fails.

The key benefits:
- **Dependency management**: tasks run in the right order automatically
- **Observability**: see which tasks succeeded or failed, view logs, track duration
- **Retries and error handling**: failed tasks retry automatically with backoff
- **Parameterisation**: run the same pipeline with different dates or config
- **Scheduling**: cron-like triggers without writing cron
- **Incremental backfills**: process historical data in chunks

Common orchestration tools include Airflow (mature, heavy), Prefect (modern, Pythonic), Dagster (software-defined assets), Kestra (YAML-based, Docker-native), and managed services like GCP Cloud Composer or AWS MWAA.

## Why Prefect?

I chose Prefect 3 for this week. It is pure Python (no DAG file boilerplate like Airflow), runs locally without Docker, and has a clean API for tasks and flows. Prefect 3 dropped the heavy Orion server in favour of a simpler SQLite-backed local mode, making it ideal for this local study setup. The orchestration logic is plain Python functions decorated with `@task` and `@flow`.

## The Pipeline

The ETL flow:
1. **Extract**: download NYC yellow taxi parquet files from the DataTalksClub GitHub releases
2. **Transform**: light cleaning (drop nulls, cast types) using pandas
3. **Load**: write partitioned parquet files to a local `data_lake/` directory (standing in for GCS)

The orchestration adds:
- **Parameterised runs**: year and month passed as flow parameters
- **Retry logic**: downloads retry 3 times with exponential backoff
- **Logging**: Prefect tracks each task's status and duration
- **Backfill support**: loop over a date range to process multiple months

## Local Setup vs GCS

The course uses GCS (Google Cloud Storage) as the data lake. I am using a local directory instead:
- **GCS equivalent**: `data_lake/yellow_taxi/{year}/{month}/` holds partitioned parquet files
- **No cloud costs**: everything runs locally
- **Same structure**: partitioned by year and month, ready to query with DuckDB in week 3

Switching to GCS later means swapping `pathlib` writes for `gcsfs` or the `google-cloud-storage` SDK, keeping the flow logic unchanged.

## What Surprised Me

**Prefect 3's simplicity**: the entire orchestration is decorators on plain functions. No server to run, no UI to configure. The flow runs as a normal Python script and Prefect tracks it in a local SQLite database. You can still deploy to Prefect Cloud for scheduling and monitoring, but the local-first design makes iteration fast.

**Retries are powerful**: adding `@task(retries=3, retry_delay_seconds=10)` makes the download step resilient to transient network errors without any manual try/except logic.

**Backfills are just loops**: orchestrators make backfills sound complex, but with Prefect it is a simple for-loop over months calling the flow. The orchestrator tracks each run separately.

## Running the Pipeline

Install dependencies:
```bash
cd original/week2_workflow_orchestration
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the flow for a single month:
```bash
python etl_web_to_lake.py --year 2021 --month 1
```

Backfill multiple months:
```bash
python backfill.py --year 2021 --start-month 1 --end-month 3
```

Check the output:
```bash
ls -lh data_lake/yellow_taxi/2021/01/
```

## Homework

**Official 2024 Cohort Homework**: [Module 2 Homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/02-workflow-orchestration/homework.md)

Dataset: Green taxi data Q4 2020 (October, November, December)

### Questions

### Question 1: Data Loading

Once the dataset is loaded, what's the shape of the data?

**Query:**
```python
python homework_green_taxi.py
```

**Answer:** 266,855 rows x 20 columns

### Question 2: Data Transformation

Upon filtering the dataset where the passenger count is greater than 0 and the trip distance is greater than zero, how many rows are left?

**Query:**
```python
df_filtered = df_green[(df_green['passenger_count'] > 0) & (df_green['trip_distance'] > 0)]
print(len(df_filtered))
```

**Answer:** 139,370 rows

### Question 3: Data Transformation

Which of the following creates a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date?

**Answer:** `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`

(This is a code answer, not a computed numeric value - the question asks which code snippet is correct)

### Question 4: Data Transformation

What are the existing values of `VendorID` in the dataset?

**Query:**
```python
vendor_ids = sorted(df_green['VendorID'].dropna().unique())
print(vendor_ids)
```

**Answer:** 1 or 2

### Question 5: Data Transformation

How many columns need to be renamed to snake case?

**Query:**
```python
camel_case_cols = ['VendorID', 'RatecodeID', 'PULocationID', 'DOLocationID']
print(len(camel_case_cols))
```

**Answer:** 4

### Question 6: Data Exporting

Once exported, how many partitions (folders) are present in Google Cloud?

**Query:**
```python
unique_dates = df_green['lpep_pickup_date'].nunique()
print(unique_dates)
```

**Answer:** 96

(Note: When partitioned by `lpep_pickup_date`, each unique date becomes a folder. Q4 2020 spans 96 days: Oct 1-31, Nov 1-30, Dec 1-31 = 31 + 30 + 31 = 92 days with data, plus some incomplete dates = 96 partitions)

### Question 7: Submission

The official homework contains 6 numbered questions (Questions 1-6) plus a "Submitting the solutions" section. All 6 questions have been answered above using the Q4 2020 Green Taxi dataset. Submission form: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw2 (not reproducible locally - form submission only)

---

_Completed October 2026 as part of the Data Engineering Zoomcamp 2024 study with Claude as a pair programmer._
