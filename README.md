<p><a target="_blank" href="https://app.eraser.io/workspace/bqYqyZzge8nO3UiGLlIt" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

<div align="center">

# Data Engineering Zoomcamp 2024 — Study

My working notes and code as I follow the [DataTalksClub Data Engineering Zoomcamp 2024](https://dezoomcamp.streamlit.app/). A learn-in-public record, built up week by week.

[![DataTalksClub](https://img.shields.io/badge/DataTalksClub-Zoomcamp%202024-FF6B35?style=flat-square)](https://dezoomcamp.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![GCP](https://img.shields.io/badge/Google%20Cloud-Terraform%20%2F%20BigQuery-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com)

</div>

## Overview

The [Data Engineering Zoomcamp](https://dezoomcamp.streamlit.app/) is a free, hands-on course run by [DataTalksClub](https://datatalks.club/). Over seven weeks it builds an end-to-end data pipeline on the [NYC yellow taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset — containerising services with Docker, loading data into Postgres, warehousing in BigQuery, orchestrating with a workflow tool, transforming with dbt, then batch and stream processing with Spark and Kafka.

This repository is **my personal study record** as I work through the course. It is a learning project, not a finished product: code, notes and explanations are written for my own understanding and may differ from the official course materials. I am building it up one week at a time.

## Progress / Status

| Week   | Topic                        | Status | Notes                                                                                                                                                                  |
| ------ | ---------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Week 1 | Introduction & Prerequisites | Done   | Docker + Postgres notes, working ingestion pipeline and docker-compose stack (completed Jan 2024)                                                                     |
| Week 2 | Workflow Orchestration       | Done   | Prefect pipelines, NYC TLC data ingest, local Parquet data lake (completed Oct 2026)                                                                                  |
| Week 3 | Data Warehouse               | Done   | DuckDB as BigQuery substitute, partitioning, clustering, query optimisation (completed Oct 2026)                                                                      |
| Week 4 | Analytics Engineering        | Done   | dbt with dbt-duckdb, staging/fact/mart models, tests and docs (completed Oct 2026)                                                                                    |
| Week 5 | Batch Processing             | Done   | pandas batch processing (PySpark concepts), partitioned Parquet output (completed Oct 2026)                                                                           |
| Week 6 | Stream Processing            | Done   | Redpanda/Kafka producer-consumer, stateful aggregation, CI testing (completed Oct 2026)                                                                               |
| Week 7 | Project                      | Done   | [SA road crash pipeline and dashboard](original/project/README.md): Prefect, Parquet lake, dbt on DuckDB, Terraform (completed in October 2026 with Claude as a pair programmer) |

**Note**: Week 1 was completed in January 2024. Weeks 2 through 6 and the Week 7 course project were completed in October 2026 with Claude Code as a pair programmer, using local substitutes for cloud services (DuckDB for BigQuery, local Parquet for GCS, Redpanda for Kafka in CI).

## Course project

The Week 7 course project is a batch pipeline over South Australia's public road crash data, 2012 to 2025. A Prefect flow downloads and checksums ten releases from data.sa.gov.au, lands them in a year-partitioned Parquet lake, builds and tests dbt models on DuckDB, benchmarks the partitioning and clustering, and exports the numbers for a two-tile dashboard: [data-engineer-bootcamp-pink.vercel.app/project](https://data-engineer-bootcamp-pink.vercel.app/project). Terraform manages the local folders and config and, in CI, builds and runs the pipeline as a Docker container. The write-up, with the evaluation criteria, dataset licence and reproduction steps, is in [`original/project/README.md`](original/project/README.md), and the real run output is in [`original/project/RUN_LOG.md`](original/project/RUN_LOG.md). It was completed in October 2026 with Claude as a pair programmer.

## Syllabus

The seven-week outline from the course, kept here for reference.

### Week 1: Introduction & Prerequisites

- Course overview
- Introduction to GCP
- Docker and docker-compose
- Running Postgres locally with Docker
- Setting up infrastructure on GCP with Terraform
- Preparing the environment for the course

### Week 2: Workflow Orchestration

- Data Lake
- Workflow orchestration
- Introduction to the orchestration tool
- ETL with GCP
- Parametrising workflows
- Cloud and additional resources

### Week 3: Data Warehouse

- Data Warehouse
- BigQuery
- Partitioning and clustering
- BigQuery best practices
- Internals of BigQuery
- Integrating BigQuery with Airflow
- BigQuery Machine Learning

### Week 4: Analytics Engineering

- Basics of analytics engineering
- dbt (data build tool)
- BigQuery and dbt
- Postgres and dbt
- dbt models
- Testing and documenting
- Deployment to the cloud and locally
- Visualising the data with Google Data Studio and Metabase

### Week 5: Batch Processing

- Batch Processing
- What is Spark
- Spark Dataframes
- Spark SQL
- Internals: GroupBy and joins

### Week 6: Stream Processing

- Introduction to Kafka
- Schemas (Avro)
- Kafka Streams
- Kafka Connect and KSQL

### Week 7: Project

- Working on your end-to-end project (mine: [SA road crash pipeline and dashboard](original/project/README.md))

## Week 1 — Getting Started

Week 1 is the implemented part of this repo. It spins up Postgres and pgAdmin with Docker Compose, downloads NYC yellow-taxi parquet files, and loads them into the local database with SQLAlchemy. Full notes live in [`week1_introduction_and_prerequisites/README.md`](./week1_introduction_and_prerequisites/README.md).

```bash
cd week1_introduction_and_prerequisites

# 1. Create and activate a virtual environment
python3 -m venv my_venv
source my_venv/bin/activate
pip3 install -r app/requirements.txt

# 2. Start Postgres + pgAdmin (pgAdmin at http://localhost:8080)
docker-compose up -d

# 3. Download taxi data and load it into Postgres
#    (downloads parquet, then loads month-by-month via SQLAlchemy)
python3 dataset_to_postgres_parquet.py \
    --table_name yellow_taxi_trip \
    --user root --password root \
    --host localhost --port 5432 \
    --database ny_taxi \
    --download_path ./data \
    --year 2021 --start_month 1 --end_month 2

# 4. When you are done
docker-compose down
```

The `database.env` and `pgadmin.env` values (`root` / `root`, `admin@admin.com`) are the **standard DataTalksClub local-Docker tutorial defaults** — they are for a throwaway local container only, not real credentials. Do not reuse them anywhere that matters.

## Tech Stack

| Area                | Tools                                      |
| ------------------- | ------------------------------------------ |
| Language            | Python 3.9                                 |
| Data handling       | pandas, pyarrow / fastparquet, SQLAlchemy  |
| Database            | PostgreSQL 13                              |
| Database admin      | pgAdmin 4                                  |
| Containerisation    | Docker, Docker Compose                     |
| Cloud (later weeks) | Google Cloud Platform, Terraform, BigQuery |
| Data source         | NYC TLC yellow-taxi trip records           |

---

_Following the [DataTalksClub Data Engineering Zoomcamp 2024](https://dezoomcamp.streamlit.app/). This is a personal study repository._

<!--- Eraser file: https://app.eraser.io/workspace/bqYqyZzge8nO3UiGLlIt --->
