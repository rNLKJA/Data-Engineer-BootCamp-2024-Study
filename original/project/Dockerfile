# Container image for the SA road crash pipeline (Prefect flow + dbt + DuckDB).
# Build context: original/project. Data lives in the /data volume.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    SA_CRASH_DATA_DIR=/data \
    SA_CRASH_DASHBOARD_JSON=/data/export/dashboard-data.json \
    DBT_USE_COLORS=false \
    PREFECT_LOGGING_COLORS=false \
    PREFECT_HOME=/tmp/prefect

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pytest.ini Makefile ./
COPY pipeline ./pipeline
COPY dbt ./dbt
COPY tests ./tests

# Runs as root so it can write to a bind-mounted host folder owned by any uid
# (the GitHub Actions runner). The container only touches /data and /tmp.
VOLUME ["/data"]
CMD ["python", "-m", "pipeline.flow"]
