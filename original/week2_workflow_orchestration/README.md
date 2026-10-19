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

### Question 1: Number of rows processed in January 2021

Run the ETL for January 2021 and count rows:

```bash
python etl_web_to_lake.py --year 2021 --month 1
```

**Query:**
```python
import pandas as pd
df = pd.read_parquet('data_lake/yellow_taxi/2021/01/yellow_tripdata_2021-01.parquet')
print(len(df))
```

**Answer:** 1,369,769 rows

### Question 2: Backfill for Q1 2021 (Jan, Feb, Mar)

Run backfill for January through March 2021:

```bash
python backfill.py --year 2021 --start-month 1 --end-month 3
```

Count total rows across all three months:

```python
import pandas as pd
months = [1, 2, 3]
total = sum(len(pd.read_parquet(f'data_lake/yellow_taxi/2021/{m:02d}/yellow_tripdata_2021-{m:02d}.parquet')) for m in months)
print(total)
```

**Answer:** 4,666,630 rows

### Question 3: What does the `@task` decorator do?

The `@task` decorator in Prefect marks a function as an orchestrated unit of work. It enables:
- Automatic retry logic on failure
- Logging and observability (task duration, status)
- Caching (reuse results if inputs unchanged)
- Dependency tracking (Prefect knows which tasks depend on others)

Without `@task`, the function runs as plain Python with no orchestration benefits.

### Question 4: What is the purpose of parameterising workflows?

Parameterisation allows the same workflow to run with different inputs (dates, file paths, table names) without changing code. Benefits:
- **Backfills**: process historical data by looping over date ranges
- **Reusability**: one flow handles all months, not a hardcoded script per month
- **Testing**: run on small samples before processing production data
- **Scheduling**: cron triggers pass `datetime.now()` as a parameter

In this pipeline, `year` and `month` are parameters, making the flow reusable across any time period.

### Question 5: How does Prefect handle task failures and retries?

Prefect retries failed tasks automatically if `retries` is set in the `@task` decorator. Example:

```python
@task(retries=3, retry_delay_seconds=10)
def download_data(url):
    # if this raises an exception, Prefect retries up to 3 times
    # with a 10-second delay between attempts
    return requests.get(url)
```

The retry logic is exponential backoff by default. If all retries fail, the task is marked as failed and the flow either stops (default) or continues depending on the flow's error handling config.

---

_Completed October 2026 as part of the Data Engineering Zoomcamp 2024 study with Claude as a pair programmer._
