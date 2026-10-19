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

## Homework

**Official 2024 Cohort Homework**: [Module 6 Homework](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/06-streaming/homework.md)

**Note**: This homework requires Docker and Kafka/RedPanda with PySpark streaming, which has Java compatibility issues on this machine.

### Question 1: Redpanda version

Run `rpk version` inside the redpanda-1 container to get the version.

**Command:**
```bash
docker exec redpanda-1 rpk version
```

**Answer**: Not reproducible locally. Expected output format: `v22.3.5 (rev 28b2443)`

### Question 2: Creating a topic

Create a topic named `test-topic` using rpk.

**Command:**
```bash
docker exec redpanda-1 rpk topic create test-topic
```

**Answer**: Not reproducible locally. Expected: `TOPIC       STATUS
test-topic  OK`

### Question 3: Connecting to the Kafka server

Install kafka-python and connect to localhost:9092.

**Code:**
```python
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.bootstrap_connected()
```

**Answer**: Not reproducible locally. Expected: `True`

### Question 4: Sending data to the stream

Send 10 test messages with 0.05s sleep between each. How much time did it take and where was most time spent?

**Answer**: Not reproducible locally. Expected: Most time spent in `producer.flush()`, total ~0.5-1.0 seconds

### Question 5: Sending the Trip Data

Create a `green-trips` topic and stream green taxi October 2019 data. How long did it take in seconds?

**Answer**: Not reproducible locally. Expected: approximately 60-120 seconds for ~450k records

### Question 6: Parsing the data with PySpark Streaming

Read from the kafka stream with PySpark and parse the JSON schema. Count records.

**Answer**: Not reproducible locally. Requires PySpark with Kafka connector jars.

### Question 7: Most popular destination

Using PySpark Streaming, find the most popular destination (DOLocationID) by grouping with a 5-minute window based on timestamp and ordering by count.

**Code:**
```python
from pyspark.sql.functions import col, current_timestamp, window

df = df.withColumn("timestamp", current_timestamp())

popular_destinations = df \
    .groupBy(window(col("timestamp"), "5 minutes"), "DOLocationID") \
    .count() \
    .orderBy("count", ascending=False)
```

**Answer**: Not reproducible locally. Requires running PySpark Streaming with Kafka connector.

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
