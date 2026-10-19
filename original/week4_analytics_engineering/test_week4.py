"""Test week 4 analytics engineering with dbt."""

import subprocess
from pathlib import Path


def test_dbt_models_exist():
    """Verify dbt model files exist."""
    week_dir = Path(__file__).parent
    taxi_analytics = week_dir / "taxi_analytics"

    assert (taxi_analytics / "dbt_project.yml").exists()
    assert (taxi_analytics / "models" / "stg_yellow_trips.sql").exists()
    assert (taxi_analytics / "models" / "fact_trips.sql").exists()
    assert (taxi_analytics / "models" / "monthly_revenue.sql").exists()
    assert (taxi_analytics / "models" / "schema.yml").exists()


def test_profiles_yml_exists():
    """Verify profiles.yml exists."""
    week_dir = Path(__file__).parent
    assert (week_dir / "profiles.yml").exists()


def test_readme_has_homework_answers():
    """Verify README has homework answers."""
    week_dir = Path(__file__).parent
    readme = (week_dir / "README.md").read_text()

    # Check for official 2024 homework answers
    assert "22,998,722" in readme or "22998722" in readme  # Q3: fact_fhv_trips count
    assert "Yellow" in readme                               # Q4: service with most rides
