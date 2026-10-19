"""Stream processing consumer: read and aggregate taxi trip events.

Demonstrates windowed aggregation, filtering, and stateful processing.
"""

import json
from collections import defaultdict
from datetime import datetime
from kafka import KafkaConsumer


class TripAggregator:
    """Stateful aggregator for taxi trip metrics."""

    def __init__(self):
        self.total_trips = 0
        self.total_revenue = 0.0
        self.total_distance = 0.0
        self.vendor_stats = defaultdict(lambda: {'trips': 0, 'revenue': 0.0})

    def process_event(self, event):
        """Process a single trip event."""
        self.total_trips += 1
        fare = event.get('fare_amount', 0.0)
        tip = event.get('tip_amount', 0.0)
        revenue = fare + tip
        distance = event.get('trip_distance', 0.0)

        self.total_revenue += revenue
        self.total_distance += distance

        vendor_id = event.get('vendor_id')
        if vendor_id:
            self.vendor_stats[vendor_id]['trips'] += 1
            self.vendor_stats[vendor_id]['revenue'] += revenue

    def get_summary(self):
        """Get current aggregation summary."""
        avg_revenue = self.total_revenue / self.total_trips if self.total_trips > 0 else 0
        avg_distance = self.total_distance / self.total_trips if self.total_trips > 0 else 0

        return {
            'total_trips': self.total_trips,
            'total_revenue': round(self.total_revenue, 2),
            'avg_revenue': round(avg_revenue, 2),
            'total_distance': round(self.total_distance, 2),
            'avg_distance': round(avg_distance, 2),
            'vendor_stats': dict(self.vendor_stats)
        }


def create_consumer(bootstrap_servers='localhost:9092', topic='taxi-trips', group_id='taxi-consumer-group'):
    """Create Kafka consumer."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )


def consume_and_aggregate(consumer, max_messages=1000, report_interval=100):
    """Consume messages and aggregate metrics."""
    aggregator = TripAggregator()
    message_count = 0

    print(f"Consuming messages from topic '{consumer.subscription()}'...")
    print(f"Will process up to {max_messages} messages\n")

    for message in consumer:
        event = message.value
        aggregator.process_event(event)
        message_count += 1

        # Periodic reporting
        if message_count % report_interval == 0:
            summary = aggregator.get_summary()
            print(f"[{message_count} messages] " +
                  f"Trips: {summary['total_trips']}, " +
                  f"Revenue: ${summary['total_revenue']:,.2f}, " +
                  f"Avg Distance: {summary['avg_distance']:.2f} mi")

        # Stop after max_messages
        if message_count >= max_messages:
            break

    return aggregator.get_summary()


def main():
    """Main consumer entry point."""
    import sys

    bootstrap_servers = sys.argv[1] if len(sys.argv) > 1 else 'localhost:9092'
    topic = sys.argv[2] if len(sys.argv) > 2 else 'taxi-trips'
    max_messages = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

    print(f"Connecting to Kafka at {bootstrap_servers}")
    consumer = create_consumer(bootstrap_servers, topic)

    try:
        summary = consume_and_aggregate(consumer, max_messages=max_messages, report_interval=100)
        print("\n=== Final Summary ===")
        print(json.dumps(summary, indent=2))
    finally:
        consumer.close()
        print("\nConsumer closed")


if __name__ == '__main__':
    main()
