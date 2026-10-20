# SA road crash pipeline (DE Zoomcamp 2024 course project).
# Run from original/project. `make all` is the whole pipeline plus tests.
# `make setup` needs Python 3.11: pass PYTHON=/full/path/to/python3.11 if the
# python3.11 on PATH is missing or is a pyenv shim that fails.

PYTHON ?= python3.11
VENV ?= .venv
BIN := $(VENV)/bin
PY := $(BIN)/python

export SA_CRASH_DATA_DIR ?= $(CURDIR)/data
export SA_CRASH_LAKE ?= $(SA_CRASH_DATA_DIR)/lake
export SA_CRASH_WAREHOUSE ?= $(SA_CRASH_DATA_DIR)/warehouse/sa_crash.duckdb
export DBT_PROFILES_DIR ?= $(CURDIR)/dbt

.PHONY: help setup infra-local ingest dbt benchmark export test test-offline test-integration all clean screenshot serve

help:
	@echo "make setup        create $(VENV) and install pinned requirements"
	@echo "make infra-local  terraform apply of infra/terraform/local (optional; tested with Terraform 1.16)"
	@echo "make ingest       download, verify and load every release into the Parquet lake"
	@echo "make dbt          dbt build (models + data tests) into the DuckDB warehouse"
	@echo "make benchmark    partitioning/clustering benchmark on representative year-bounded queries"
	@echo "make export       write web/app/project/dashboard-data.json"
	@echo "make test         offline tests, then integration tests against the warehouse"
	@echo "make all          the whole Prefect flow, then all tests"
	@echo "make screenshot   capture images/dashboard.png from a running web server"
	@echo "make clean        delete data/ and dbt build output"

$(PY):
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt

setup: $(PY)

TF ?= $(shell command -v terraform 2>/dev/null || command -v tofu 2>/dev/null)
infra-local:
	@test -n "$(TF)" || (echo "Install Terraform 1.16 first (brew install hashicorp/tap/terraform); OpenTofu is untested"; exit 1)
	cd infra/terraform/local && $(TF) init -input=false && $(TF) apply -input=false -auto-approve && $(TF) output

ingest: $(PY)
	$(PY) -m pipeline.flow --stage ingest

dbt: $(PY)
	$(PY) -m pipeline.flow --stage dbt

benchmark: $(PY)
	$(PY) -m pipeline.flow --stage benchmark

export: $(PY)
	$(PY) -m pipeline.flow --stage export

test-offline: $(PY)
	$(PY) -m pytest -m "not integration" -v

test-integration: $(PY)
	$(PY) -m pytest -m integration -v

test: test-offline test-integration

all: $(PY)
	$(PY) -m pipeline.flow
	$(MAKE) test

serve: $(PY)
	$(PY) -m pipeline.serve

screenshot:
	node scripts/capture_dashboard.mjs $${DASHBOARD_URL:-http://localhost:3832/project} images/dashboard.png

clean:
	rm -rf data dbt/target dbt/logs
