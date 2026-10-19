"""Stream processing producer: send taxi trip events to Redpanda/Kafka.

Simulates real-time taxi trip events by reading historical data
and streaming it with realistic timing.
"""

import json
import time
from pathlib import Path
from kafka import KafkaProducer
import pandas as pd


def create_producer(bootstrap_servers='localhost:9092'):
    """Create Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None
    )


def load_sample_data(n_records=1000):
    """Load sample taxi data for streaming simulation."""
    week2_dir = Path(__file__).parent.parent.parent / "original/week2_workflow_orchestration/downloads"
    parquet_files = list(week2_dir.glob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(f"No Parquet files found in {week2_dir}")

    # Read first file, take n_records
    df = pd.read_parquet(parquet_files[0])
    return df.head(n_records)


def stream_taxi_trips(producer, topic='taxi-trips', delay_ms=10):
    """Stream taxi trips to Kafka topic."""
    print(f"Loading sample data...")
    df = load_sample_data(n_records=1000)
    print(f"Streaming {len(df)} records to topic '{topic}'...")

    sent_count = 0
    for idx, row in df.iterrows():
        # Create event payload
        event = {
            'trip_id': f"{row['VendorID']}_{idx}",
            'vendor_id': int(row['VendorID']),
            'pickup_datetime': row['tpep_pickup_datetime'].isoformat(),
            'dropoff_datetime': row['tpep_dropoff_datetime'].isoformat() if pd.notna(row['tpep_dropoff_datetime']) else None,
            'passenger_count': int(row['passenger_count']) if pd.notna(row['passenger_count']) else 0,
            'trip_distance': float(row['trip_distance']),
            'fare_amount': float(row['fare_amount']),
            'tip_amount': float(row['tip_amount']) if 'tip_amount' in row and pd.notna(row['tip_amount']) else 0.0,
        }

        # Send to Kafka
        key = str(row['VendorID'])
        producer.send(topic, key=key, value=event)
        sent_count += 1

        if sent_count % 100 == 0:
            print(f"  Sent {sent_count} events...")

        # Small delay to simulate streaming
        time.sleep(delay_ms / 1000.0)

    producer.flush()
    print(f"✓ Sent {sent_count} events to '{topic}'")
    return sent_count


def main():
    """Main producer entry point."""
    import sys

    bootstrap_servers = sys.argv[1] if len(sys.argv) > 1 else 'localhost:9092'
    topic = sys.argv[2] if len(sys.argv) > 2 else 'taxi-trips'

    print(f"Connecting to Kafka at {bootstrap_servers}")
    producer = create_producer(bootstrap_servers)

    try:
        stream_taxi_trips(producer, topic, delay_ms=10)
    finally:
        producer.close()
        print("Producer closed")


if __name__ == '__main__':
    main()
