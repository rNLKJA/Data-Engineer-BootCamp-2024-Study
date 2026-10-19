"""Paths and settings for the SA road crash pipeline.

Every path can be overridden with an environment variable so the same code runs
on a laptop, in GitHub Actions and inside the Docker image. Defaults resolve
relative to ``original/project`` so a clean clone works without any setup.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# original/project sits two levels below the repository root. Inside the Docker
# image the project is /app, which has no such parents; SA_CRASH_DASHBOARD_JSON
# is set there instead.
REPO_ROOT = PROJECT_ROOT.parents[1] if len(PROJECT_ROOT.parents) > 1 else PROJECT_ROOT


def _path(env_name: str, default: Path) -> Path:
    value = os.environ.get(env_name)
    return Path(value).expanduser().resolve() if value else default.resolve()


@dataclass(frozen=True)
class Settings:
    """Resolved locations used by every pipeline step."""

    data_dir: Path
    landing_dir: Path
    lake_dir: Path
    warehouse_path: Path
    sources_path: Path
    dbt_project_dir: Path
    dbt_profiles_dir: Path
    dashboard_json: Path
    benchmark_dir: Path

    @property
    def raw_dir(self) -> Path:
        return self.lake_dir / "raw"

    @property
    def curated_dir(self) -> Path:
        return self.lake_dir / "curated"

    def dbt_env(self) -> dict[str, str]:
        """Environment variables the dbt project reads through ``env_var()``."""
        return {
            "SA_CRASH_LAKE": str(self.lake_dir),
            "SA_CRASH_WAREHOUSE": str(self.warehouse_path),
        }


def load_settings() -> Settings:
    data_dir = _path("SA_CRASH_DATA_DIR", PROJECT_ROOT / "data")
    lake_dir = _path("SA_CRASH_LAKE", data_dir / "lake")
    warehouse_path = _path("SA_CRASH_WAREHOUSE", data_dir / "warehouse" / "sa_crash.duckdb")
    return Settings(
        data_dir=data_dir,
        landing_dir=_path("SA_CRASH_LANDING", data_dir / "landing"),
        lake_dir=lake_dir,
        warehouse_path=warehouse_path,
        sources_path=_path("SA_CRASH_SOURCES", PROJECT_ROOT / "pipeline" / "sources.yml"),
        dbt_project_dir=_path("SA_CRASH_DBT_PROJECT_DIR", PROJECT_ROOT / "dbt"),
        dbt_profiles_dir=_path("DBT_PROFILES_DIR", PROJECT_ROOT / "dbt"),
        dashboard_json=_path(
            "SA_CRASH_DASHBOARD_JSON",
            REPO_ROOT / "web" / "app" / "project" / "dashboard-data.json",
        ),
        benchmark_dir=_path("SA_CRASH_BENCHMARK_DIR", warehouse_path.parent),
    )
