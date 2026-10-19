"""Test week 5 batch processing."""

from pathlib import Path


def test_batch_script_exists():
    """Verify batch processing script exists."""
    week_dir = Path(__file__).parent
    assert (week_dir / "batch_process.py").exists()
    assert (week_dir / "requirements.txt").exists()


def test_run_log_exists():
    """Verify RUN_LOG.md was generated."""
    week_dir = Path(__file__).parent
    run_log = week_dir / "RUN_LOG.md"
    assert run_log.exists()

    content = run_log.read_text()
    assert "Homework Answers" in content
    assert "84,001,487" in content or "84001487" in content  # Q1 revenue


def test_output_partitions_exist():
    """Verify partitioned output was created."""
    week_dir = Path(__file__).parent
    output_dir = week_dir / "output/taxi_processed"

    # Check year=2021 partitions exist
    assert (output_dir / "year=2021/month=1/data.parquet").exists()
    assert (output_dir / "year=2021/month=2/data.parquet").exists()
    assert (output_dir / "year=2021/month=3/data.parquet").exists()


def test_readme_has_homework_answers():
    """Verify README has homework answers."""
    week_dir = Path(__file__).parent
    readme = (week_dir / "README.md").read_text()

    assert "84,001,487" in readme or "84001487" in readme  # Q1 revenue
    assert "1,343,375" in readme or "1343375" in readme    # Jan trips
    assert "4.45" in readme                                 # March avg distance
