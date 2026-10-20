"""Prefect 3 flow: DIT zips -> Parquet lake -> dbt (DuckDB) -> benchmark -> dashboard JSON.

Run everything:            python -m pipeline.flow
Run one stage:             python -m pipeline.flow --stage ingest|dbt|benchmark|export

Prefect runs in ephemeral local mode (a temporary local API server that the
flow starts and stops itself), so no Prefect Cloud account or server is needed.
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from prefect import flow, get_run_logger, task
from prefect.cache_policies import NONE

from pipeline import benchmark, export_dashboard
from pipeline.config import Settings, load_settings
from pipeline.dbt_runner import run_dbt
from pipeline.ingest import (
    extract_release,
    fetch_release,
    lake_partitions,
    load_to_lake,
    prune_stale_partitions,
    validate_schema,
    write_release_manifest,
)
from pipeline.sources import Release, load_manifest

STAGES = ("all", "ingest", "dbt", "benchmark", "export")


@task(name="fetch_release", retries=2, retry_delay_seconds=10, cache_policy=NONE)
def fetch_release_task(release: Release, landing_dir: Path) -> Path:
    logger = get_run_logger()
    result = fetch_release(release, landing_dir)
    source = "cache hit" if result.cached else "downloaded"
    logger.info("%s: %s %s (%d bytes, sha256 %s...)", release.release_id, source,
                result.path.name, result.bytes, result.sha256[:12])  # fmt: skip
    return result.path


@task(name="validate_schema", cache_policy=NONE)
def validate_schema_task(zip_path: Path, release: Release, work_dir: Path) -> dict[str, Path]:
    logger = get_run_logger()
    csv_paths = extract_release(zip_path, release, work_dir)
    counts = validate_schema(csv_paths, release)
    logger.info("%s: header contract ok; rows crash=%d casualty=%d units=%d",
                release.release_id, counts["crash"], counts["casualty"], counts["units"])  # fmt: skip
    return csv_paths


@task(name="load_to_lake", cache_policy=NONE)
def load_to_lake_task(csv_paths: dict[str, Path], release: Release, raw_dir: Path) -> dict[str, int]:
    logger = get_run_logger()
    written = load_to_lake(csv_paths, release, raw_dir)
    logger.info("%s: wrote years %d-%d to lake; crash=%d casualty=%d units=%d",
                release.release_id, release.first_year, release.last_year,
                written["crash"], written["casualty"], written["units"])  # fmt: skip
    return written


@task(name="dbt_build", cache_policy=NONE)
def dbt_build_task(settings: Settings) -> dict[str, int]:
    logger = get_run_logger()
    os.environ.update(settings.dbt_env())
    settings.warehouse_path.parent.mkdir(parents=True, exist_ok=True)
    settings.curated_dir.mkdir(parents=True, exist_ok=True)
    outcome = run_dbt(
        [
            "build",
            "--project-dir", str(settings.dbt_project_dir),
            "--profiles-dir", str(settings.dbt_profiles_dir),
        ]  # fmt: skip
    )
    logger.info("dbt build finished: %s", ", ".join(f"{k}={v}" for k, v in outcome.statuses.items()))
    if not outcome.success:
        raise RuntimeError(f"dbt build failed: {outcome.statuses or outcome.exception}")
    return outcome.statuses


@task(name="benchmark_warehouse", cache_policy=NONE)
def benchmark_task(settings: Settings) -> Path:
    return benchmark.run(settings)


@task(name="export_dashboard", cache_policy=NONE)
def export_dashboard_task(settings: Settings) -> Path:
    logger = get_run_logger()
    path = export_dashboard.export(settings)
    logger.info("dashboard JSON written to %s (%d bytes)", path, path.stat().st_size)
    return path


@flow(name="sa_crash_pipeline", log_prints=True)
def sa_crash_pipeline(stage: str = "all") -> None:
    """Batch pipeline for the SA road crash releases.

    ``stage`` limits the run to one step; ``all`` runs the whole DAG in order.
    """
    if stage not in STAGES:
        raise ValueError(f"stage must be one of {STAGES}")
    logger = get_run_logger()
    settings = load_settings()
    manifest = load_manifest(settings.sources_path)
    logger.info("manifest: %d releases covering %d-%d (%d years)", len(manifest.releases),
                min(manifest.years), max(manifest.years), len(manifest.years))  # fmt: skip

    if stage in ("all", "ingest"):
        with tempfile.TemporaryDirectory(prefix="sa_crash_") as work:
            for release in manifest.releases:
                zip_path = fetch_release_task(release, settings.landing_dir)
                csv_paths = validate_schema_task(zip_path, release, Path(work))
                load_to_lake_task(csv_paths, release, settings.raw_dir)
        removed = prune_stale_partitions(manifest, settings.raw_dir)
        write_release_manifest(manifest, settings.raw_dir)
        years = lake_partitions(settings.raw_dir)
        logger.info("lake has %d crash year partitions (%d-%d); removed %d stale",
                    len(years), years[0], years[-1], len(removed))  # fmt: skip

    if stage in ("all", "dbt"):
        dbt_build_task(settings)
    if stage in ("all", "benchmark"):
        benchmark_task(settings)
    if stage in ("all", "export"):
        export_dashboard_task(settings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--stage", choices=STAGES, default="all")
    args = parser.parse_args(argv)
    sa_crash_pipeline(stage=args.stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
