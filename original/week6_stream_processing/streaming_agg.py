"""
Streaming aggregation with windowing and state management
Demonstrates real-time analytics patterns with Kafka streams.
"""

from kafka import KafkaConsumer
import json
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List


class StreamingAggregator:
    """
    Maintains sliding window aggregations over streaming taxi events

    Tracks:
    - Trip count per 5-minute window
    - Revenue per window
    - Average distance per window
    """

    def __init__(self, window_minutes: int = 5):
        self.window_minutes = window_minutes
        self.windows: Dict[datetime, List[dict]] = defaultdict(list)

    def get_window_key(self, timestamp: datetime) -> datetime:
        """Round timestamp down to window boundary"""
        minutes = (timestamp.minute // self.window_minutes) * self.window_minutes
        return timestamp.replace(minute=minutes, second=0, microsecond=0)

    def add_event(self, event: dict) -> None:
        """Add event to appropriate window"""
        pickup_time = datetime.fromisoformat(event["tpep_pickup_datetime"])
        window_key = self.get_window_key(pickup_time)
        self.windows[window_key].append(event)

    def compute_window_stats(self, window_key: datetime) -> dict:
        """Compute aggregated stats for a window"""
        events = self.windows[window_key]
        if not events:
            return {
                "window_start": window_key.isoformat(),
                "trip_count": 0,
                "total_revenue": 0.0,
                "avg_distance": 0.0,
            }

        total_revenue = sum(e.get("total_amount", 0) for e in events)
        total_distance = sum(e.get("trip_distance", 0) for e in events)
        trip_count = len(events)

        return {
            "window_start": window_key.isoformat(),
            "trip_count": trip_count,
            "total_revenue": round(total_revenue, 2),
            "avg_distance": round(total_distance / trip_count, 2) if trip_count else 0,
        }

    def get_all_window_stats(self) -> List[dict]:
        """Get stats for all windows, sorted by time"""
        window_keys = sorted(self.windows.keys())
        return [self.compute_window_stats(wk) for wk in window_keys]

    def prune_old_windows(self, cutoff_time: datetime) -> None:
        """Remove windows older than cutoff (memory management)"""
        old_windows = [wk for wk in self.windows.keys() if wk < cutoff_time]
        for wk in old_windows:
            del self.windows[wk]


def run_streaming_aggregation(
    topic: str = "taxi_rides",
    bootstrap_servers: str = "localhost:9092",
    duration_seconds: int = 60,
) -> None:
    """
    Run streaming aggregation demo

    Consumes from Kafka topic and maintains sliding window aggregations.
    In production, this would run continuously with checkpointing.
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="streaming_aggregator",
    )

    aggregator = StreamingAggregator(window_minutes=5)
    start_time = datetime.now()

    print("=" * 80)
    print("Streaming Aggregation Demo")
    print("=" * 80)
    print(f"Consuming from topic: {topic}")
    print(f"Window size: 5 minutes")
    print(f"Duration: {duration_seconds}s\n")

    try:
        for message in consumer:
            event = message.value
            aggregator.add_event(event)

            # Print window stats every 10 events
            if len(aggregator.windows) > 0 and message.offset % 10 == 0:
                stats = aggregator.get_all_window_stats()
                latest = stats[-1] if stats else {}
                print(
                    f"Offset {message.offset:>5} | "
                    f"Windows: {len(aggregator.windows)} | "
                    f"Latest window trips: {latest.get('trip_count', 0)}"
                )

            # Stop after duration
            if (datetime.now() - start_time).seconds >= duration_seconds:
                break

            # Prune old windows (keep last 1 hour)
            cutoff = datetime.now() - timedelta(hours=1)
            aggregator.prune_old_windows(cutoff)

    except KeyboardInterrupt:
        print("\nStopped by user")

    finally:
        consumer.close()

    # Print final window statistics
    print("\n" + "=" * 80)
    print("Final Window Statistics")
    print("=" * 80)
    for stat in aggregator.get_all_window_stats()[:10]:  # Show first 10 windows
        print(
            f"{stat['window_start']}: "
            f"{stat['trip_count']} trips | "
            f"${stat['total_revenue']:.2f} revenue | "
            f"{stat['avg_distance']:.2f} mi avg"
        )


if __name__ == "__main__":
    # Run streaming aggregation for 60 seconds
    # This requires producer.py to be running first
    try:
        run_streaming_aggregation(duration_seconds=60)
    except Exception as e:
        print(f"Error: {e}")
        print(
            "Make sure Redpanda/Kafka is running and producer.py has published events."
        )
