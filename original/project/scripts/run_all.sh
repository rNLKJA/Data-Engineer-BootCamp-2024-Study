#!/usr/bin/env bash
# Run `make all` from a clean data directory and capture the terminal output
# into RUN_LOG.md. Usage (from original/project):
#   scripts/run_all.sh           keep data/landing (the download cache)
#   scripts/run_all.sh --fresh   also delete data/landing, so every release is downloaded
set -euo pipefail
cd "$(dirname "$0")/.."
fresh="${1:-}"

export DBT_USE_COLORS=false
export PREFECT_LOGGING_COLORS=false
log="$(mktemp)"

{
  echo "\$ date -u"; date -u
  echo "\$ uname -sm"; uname -sm
  echo "\$ .venv/bin/python --version"; .venv/bin/python --version
  if [ "$fresh" = "--fresh" ]; then
    echo "\$ rm -rf data/landing data/lake data/warehouse dbt/target"
    rm -rf data/landing data/lake data/warehouse dbt/target
  else
    echo "\$ rm -rf data/lake data/warehouse dbt/target   # keep data/landing (the download cache)"
    rm -rf data/lake data/warehouse dbt/target
  fi
  echo "\$ ls -l data/landing"; ls -l data/landing 2>/dev/null || echo "(empty: first run downloads every release)"
  echo "\$ make all"
  start=$(date +%s)
  make all
  echo "make all finished in $(( $(date +%s) - start ))s"
  echo "\$ du -sh data/landing data/lake/raw data/lake/curated data/warehouse/sa_crash.duckdb"
  du -sh data/landing data/lake/raw data/lake/curated data/warehouse/sa_crash.duckdb
} 2>&1 | tee "$log"

{
  echo "# Run log"
  echo
  echo "Real terminal output of \`scripts/run_all.sh\` (which runs \`make all\`) on the machine"
  echo "and date shown below. Nothing here is edited except that this header was added."
  echo
  echo '```text'
  cat "$log"
  echo '```'
} > RUN_LOG.md
rm -f "$log"
echo "wrote RUN_LOG.md"
