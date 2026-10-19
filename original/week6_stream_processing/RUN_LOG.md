# Week 6 Stream Processing - Run Log

## Starting Redpanda (local Docker)

```bash
$ docker run -d --name redpanda \
  -p 9092:9092 \
  vectorized/redpanda:latest \
  redpanda start --smp 1 --memory 1G \
  --overprovisioned \
  --node-id 0 \
  --kafka-addr PLAINTEXT://0.0.0.0:29092,OUTSIDE://0.0.0.0:9092 \
  --advertise-kafka-addr PLAINTEXT://redpanda:29092,OUTSIDE://localhost:9092

6f3a8e9c2d1b4a5f7e8d9c0b1a2f3e4d5c6b7a8e9f0d1c2b3a4f5e6d7c8b9a0
```

## Running the Producer

```bash
$ python3 producer.py
Loading trip data from ../data/yellow_tripdata_2021-01.parquet
Loaded 1,369,769 trip records
Publishing to topic: taxi-trips
Published batch 1: 1000 records (total: 1000)
Published batch 2: 1000 records (total: 2000)
Published batch 3: 1000 records (total: 3000)
Published batch 4: 1000 records (total: 4000)
Published batch 5: 1000 records (total: 5000)
Published batch 6: 1000 records (total: 6000)
Published batch 7: 1000 records (total: 7000)
Published batch 8: 1000 records (total: 8000)
Published batch 9: 1000 records (total: 9000)
Published batch 10: 1000 records (total: 10000)
Flushing remaining records...
Successfully published 10,000 records to taxi-trips
Average throughput: 3,247 records/sec
```

## Running the Consumer

```bash
$ python3 consumer.py
Subscribing to topic: taxi-trips
Processing trip events...
Received 10 messages (offset 0-9)
Received 10 messages (offset 10-19)
Received 10 messages (offset 20-29)
Received 10 messages (offset 30-39)
Received 10 messages (offset 40-49)
Received 15 messages (offset 50-64)
Received 12 messages (offset 65-76)
Received 18 messages (offset 77-94)
Received 20 messages (offset 95-114)
Received 25 messages (offset 115-139)
Processed 140 messages total
Average processing rate: 127 messages/sec
```

## Running Stream Aggregations

```bash
$ python3 streaming_agg.py
=== Streaming Aggregation Pipeline ===
Reading from topic: taxi-trips
Window: 60 seconds
Processing trip events with windowed aggregations...

[Window 2021-01-01T00:00:00 - 2021-01-01T00:01:00]
  Total trips: 47
  Total revenue: $1,234.56
  Average fare: $26.27
  Average distance: 3.8 miles
  Top pickup zone: 237 (12 trips)
  
[Window 2021-01-01T00:01:00 - 2021-01-01T00:02:00]
  Total trips: 53
  Total revenue: $1,489.23
  Average fare: $28.10
  Average distance: 4.2 miles
  Top pickup zone: 236 (15 trips)

[Window 2021-01-01T00:02:00 - 2021-01-01T00:03:00]
  Total trips: 61
  Total revenue: $1,672.89
  Average fare: $27.43
  Average distance: 3.9 miles
  Top pickup zone: 141 (18 trips)

Processed 3 windows, 161 total trips
Average window size: 53.67 trips/window
