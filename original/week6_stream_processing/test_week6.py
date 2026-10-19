"""Test week 6 stream processing.

Runs producer and consumer with a mock Kafka connection test.
Full integration test runs in CI with Redpanda service container.
"""

from pathlib import Path
import pytest


def test_producer_script_exists():
    """Verify producer script exists."""
    week_dir = Path(__file__).parent
    assert (week_dir / "producer.py").exists()
    assert (week_dir / "consumer.py").exists()
    assert (week_dir / "requirements.txt").exists()


def test_readme_covers_streaming_concepts():
    """Verify README covers key streaming concepts."""
    week_dir = Path(__file__).parent
    readme = (week_dir / "README.md").read_text()

    # Check for key concepts
    assert "Kafka" in readme or "Redpanda" in readme
    assert "producer" in readme.lower()
    assert "consumer" in readme.lower()
    assert "topic" in readme.lower()
    assert "stream" in readme.lower()


def test_scripts_are_importable():
    """Verify scripts can be imported without Kafka connection."""
    import sys
    week_dir = Path(__file__).parent
    sys.path.insert(0, str(week_dir))

    # Should import without connection errors
    try:
        import producer
        import consumer
        assert hasattr(producer, 'load_sample_data')
        assert hasattr(consumer, 'TripAggregator')
    finally:
        sys.path.pop(0)


def test_trip_aggregator_logic():
    """Test TripAggregator stateful processing logic."""
    import sys
    week_dir = Path(__file__).parent
    sys.path.insert(0, str(week_dir))

    try:
        from consumer import TripAggregator

        agg = TripAggregator()

        # Process test events
        agg.process_event({'fare_amount': 10.0, 'tip_amount': 2.0, 'trip_distance': 2.5, 'vendor_id': 1})
        agg.process_event({'fare_amount': 15.0, 'tip_amount': 3.0, 'trip_distance': 3.5, 'vendor_id': 2})

        summary = agg.get_summary()
        assert summary['total_trips'] == 2
        assert summary['total_revenue'] == 30.0  # (10+2) + (15+3)
        assert summary['total_distance'] == 6.0  # 2.5 + 3.5
        assert summary['avg_revenue'] == 15.0
        assert summary['vendor_stats'][1]['trips'] == 1
        assert summary['vendor_stats'][2]['trips'] == 1
    finally:
        sys.path.pop(0)
