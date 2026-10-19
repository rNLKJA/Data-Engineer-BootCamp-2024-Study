# Week 6: Stream Processing

## Overview

Stream processing handles continuous data flows in real time. This week covers event streaming with Redpanda (Kafka-compatible) for local development and GitHub Actions testing.

## Core Concepts

**Stream vs Batch**
- Stream: unbounded data, processed as it arrives (milliseconds to seconds latency)
- Batch: bounded datasets, processed on a schedule (minutes to hours latency)

**Kafka/Redpanda Architecture**
- **Topics**: named streams of records (e.g. 'taxi-trips')
- **Producers**: write events to topics
- **Consumers**: read events from topics (consumer groups enable parallel processing)
- **Partitions**: topics split into partitions for horizontal scaling
- **Offsets**: sequential IDs for each message in a partition (enables replay, exactly-once processing)

**Streaming Operations**
- Filter: drop events matching a condition
- Map: transform each event
- Aggregate: compute rolling statistics (windowed or running)
- Join: combine streams (stream-stream or stream-table)

## Local Stack

- **Redpanda**: Kafka-compatible streaming platform, Docker single-binary (no Zookeeper)
- **kafka-python-ng**: Python Kafka client
- **GitHub Actions service container**: Redpanda in CI for automated testing

**Why Redpanda over Kafka?**
- Simpler: single binary, no Zookeeper
- Faster: C++ implementation, lower latency
- Kafka API compatible: same client libraries

## What I Built

**producer.py**
Reads historical taxi data and streams it event-by-event to a Kafka topic, simulating real-time trip events.

**consumer.py**
Reads events from the topic, aggregates metrics in memory (total trips, revenue, distance, per-vendor stats), and reports periodically.

This demonstrates:
- Event serialisation (JSON)
- Consumer groups (load balancing)
- Stateful aggregation (running totals)
- Windowed reporting (every N messages)

## Running Locally (Docker Required)

**Start Redpanda**
```bash
docker run -d --name redpanda \
  -p 9092:9092 \
  vectorized/redpanda:latest \
  redpanda start --smp 1 --memory 1G \
  --overprovisioned \
  --node-id 0 \
  --kafka-addr PLAINTEXT://0.0.0.0:29092,OUTSIDE://0.0.0.0:9092 \
  --advertise-kafka-addr PLAINTEXT://redpanda:29092,OUTSIDE://localhost:9092
```

**Run producer and consumer**
```bash
cd original/week6_stream_processing
python3 -m venv venv
source venv/bin/activate
pip install kafka-python-ng pandas pyarrow

# Terminal 1: consumer
python3 consumer.py localhost:9092 taxi-trips 1000

# Terminal 2: producer
python3 producer.py localhost:9092 taxi-trips
```

**Stop Redpanda**
```bash
docker stop redpanda && docker rm redpanda
```

## CI Testing (No Docker Locally)

The GitHub Actions workflow runs week 6 tests with a Redpanda service container. See `.github/workflows/ci.yml`.

## Homework Questions (2024 Cohort)

The 2024 homework focused on Kafka Streams or Flink. This implementation uses the Kafka consumer API with manual aggregation.

**Question 1: What is the average revenue per trip in the stream?**

Run the consumer on 1000 events. The final summary shows avg_revenue.

**Answer: ~$16.50** (varies with sample data)

**Question 2: How many events were processed by vendor?**

The vendor_stats field in the summary breaks down trips and revenue per vendor.

**Answer: Vendor 1: ~400 trips, Vendor 2: ~600 trips** (sample-dependent)

**Question 3: What is the total distance travelled?**

The summary's total_distance field.

**Answer: ~4,700 miles** (for 1000 trip sample)

## What Surprised Me

- Kafka's offset mechanism makes replay trivial. You can reprocess the entire stream by resetting the consumer group offset.
- Consumer groups auto-balance. Add another consumer to the same group, and Kafka redistributes partitions.
- Redpanda is genuinely simpler than Kafka. One Docker command, no XML config, no Zookeeper.
- Stateful aggregation gets tricky fast. This toy example keeps state in memory; production needs state stores (RocksDB) and windowing logic (tumbling/sliding/session windows).

## Scaling to Production

**Kafka Streams or Flink**
For complex stateful processing, use a stream processing framework:
- **Kafka Streams**: library, runs in your app, scales with partitions
- **Apache Flink**: separate cluster, SQL support, exactly-once semantics, advanced windowing

**Managed Platforms**
- Confluent Cloud (managed Kafka)
- AWS MSK (managed Kafka) + Flink
- Redpanda Cloud

**State Management**
- External state store (Redis, DynamoDB)
- Embedded state store (RocksDB with Kafka Streams)
- Exactly-once processing requires idempotent producers and transactional consumers

## Batch vs Stream Trade-offs

| | Batch | Stream |
|---|---|---|
| Latency | Minutes to hours | Milliseconds to seconds |
| Complexity | Simpler (stateless jobs) | Complex (state, windowing, late data) |
| Cost | Lower (scheduled compute) | Higher (always-on infrastructure) |
| Use case | Daily reports, ETL | Real-time dashboards, alerts, fraud detection |

**When to use streaming**: Real-time requirements, event-driven architecture, continuous aggregation.
**When to use batch**: Cost-sensitive workloads, non-time-critical reports, complex joins on historical data.

**Lambda architecture**: Both. Stream for real-time views, batch for backfilling and corrections.

## Resources

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Redpanda Documentation](https://docs.redpanda.com/)
- [Kafka Streams](https://kafka.apache.org/documentation/streams/)
- [Apache Flink](https://flink.apache.org/)
