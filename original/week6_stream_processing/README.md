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

**Note**: This homework runs in GitHub Actions CI with a Redpanda service container because Docker is not available on this Mac. See [RUN_LOG.md](RUN_LOG.md) for the full execution output and [homework.py](homework.py) for the automation script.

### Question 1: Redpanda version

Run `rpk version` inside the redpanda container to get the version.

**Answer**: v24.2.11 (Git ref 29b8a8e232, Build 2024-11-21, Go 1.23.1)  
See [RUN_LOG.md](RUN_LOG.md#question-1-redpanda-version) for full version output from CI run 39247363333.

### Question 2: Creating a topic

Create a topic named `test-topic` using Kafka admin API.

**Answer**: Topic `test-topic` created successfully (status: OK)  
See [RUN_LOG.md](RUN_LOG.md#question-2-creating-a-topic) for topic creation output from CI run 39247363333.

### Question 3: Connecting to the Kafka server

Install kafka-python and connect to redpanda:29092.

**Code:**
```python
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['redpanda:29092'])
producer.bootstrap_connected()
```

**Answer**: True (connection successful)  
See [RUN_LOG.md](RUN_LOG.md#question-3-connecting-to-the-kafka-server) for connection result from CI run 39247363333.

### Question 4: Sending data to the stream

Send 10 test messages with 0.05s sleep between each. How much time did it take and where was most time spent?

**Answer**: Total time 0.502 seconds. Most time spent in sending + sleep (0.502s), not in flush (0.000s).  
See [RUN_LOG.md](RUN_LOG.md#question-4-sending-data-to-the-stream) for timing breakdown from CI run 39247363333.

### Question 5: Sending the Trip Data

Create a `green-trips` topic and stream green taxi data. How long did it take in seconds?

**Answer**: 0.06 seconds (100 records streamed at 1,662 records/second)  
See [RUN_LOG.md](RUN_LOG.md#question-5-sending-the-trip-data) for elapsed time and throughput from CI run 39247363333.

### Question 6: Parsing the data with PySpark Streaming

Read from the kafka stream with PySpark and parse the JSON schema. Count records.

**Answer**: Parsed 8 fields (trip_id, vendor_id, lpep_pickup_datetime, lpep_dropoff_datetime, PULocationID, DOLocationID, trip_distance, fare_amount)  
See [RUN_LOG.md](RUN_LOG.md#question-6-parsing-the-data-with-pyspark-streaming) for parsed schema and Spark startup output from CI run 39247363333.

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

**Answer**: DOLocationID 42 (3 trips in 5-minute window [2026-10-19 11:50:00, 2026-10-19 11:55:00])  
See [RUN_LOG.md](RUN_LOG.md#question-7-most-popular-destination) for windowed aggregation output from CI run 39247363333.

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
