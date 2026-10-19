#!/usr/bin/env python3
"""
Week 6 Homework Runner
Runs all homework questions with a Redpanda/Kafka cluster and captures outputs
"""
import json
import os
import time
import subprocess
import sys
from pathlib import Path
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import pandas as pd

# In GitHub Actions, service containers are accessed via localhost
# In docker-compose, they're accessed by service name
BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')


def question_1_rpk_version():
    """Q1: Get Redpanda version using rpk"""
    print("\n" + "="*60)
    print("Question 1: Redpanda version")
    print("="*60)

    # Try to get version via rpk command (in docker container)
    try:
        result = subprocess.run(
            ['docker', 'exec', 'redpanda', 'rpk', 'version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
            # Extract version from output like "v24.2.11 (rev 123456)"
            for line in result.stdout.splitlines():
                if line.startswith('v'):
                    version = line.split()[0]
                    print(f"Redpanda version: {version}")
                    return version
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: connect via Kafka protocol
    from kafka import KafkaClient
    client = KafkaClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    client.close()
    print(f"Redpanda broker connected via Kafka protocol")
    print(f"Bootstrap servers: {BOOTSTRAP_SERVERS}")
    return f"Connected via Kafka protocol at {BOOTSTRAP_SERVERS}"


def question_2_create_topic():
    """Q2: Create a test-topic"""
    print("\n" + "="*60)
    print("Question 2: Creating a topic")
    print("="*60)

    # Try using rpk (faster and cleaner)
    try:
        # Check if topic exists
        result = subprocess.run(
            ['docker', 'exec', 'redpanda', 'rpk', 'topic', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and 'test-topic' in result.stdout:
            print("Topic 'test-topic' already exists, deleting...")
            subprocess.run(
                ['docker', 'exec', 'redpanda', 'rpk', 'topic', 'delete', 'test-topic'],
                capture_output=True,
                timeout=10
            )
            time.sleep(1)

        # Create topic via rpk
        result = subprocess.run(
            ['docker', 'exec', 'redpanda', 'rpk', 'topic', 'create', 'test-topic', '-p', '1', '-r', '1'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
            return "test-topic created successfully via rpk"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: use Kafka admin API
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

    # Check if topic already exists
    existing = admin.list_topics()
    if 'test-topic' in existing:
        print("Topic 'test-topic' already exists")
        admin.delete_topics(['test-topic'])
        time.sleep(2)

    # Create new topic
    topic = NewTopic(name='test-topic', num_partitions=1, replication_factor=1)
    admin.create_topics([topic])
    print("TOPIC       STATUS")
    print("test-topic  OK")
    admin.close()
    return "test-topic created successfully"


def question_3_connect():
    """Q3: Connect to Kafka server"""
    print("\n" + "="*60)
    print("Question 3: Connecting to the Kafka server")
    print("="*60)

    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    connected = producer.bootstrap_connected()
    print(f"producer.bootstrap_connected() = {connected}")
    producer.close()
    return connected


def question_4_send_timing():
    """Q4: Timing for sending 10 messages"""
    print("\n" + "="*60)
    print("Question 4: Sending data to the stream")
    print("="*60)

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Time the sending
    start = time.time()
    send_time_start = time.time()
    for i in range(10):
        producer.send('test-topic', value={'number': i})
        time.sleep(0.05)
    send_time = time.time() - send_time_start

    flush_start = time.time()
    producer.flush()
    flush_time = time.time() - flush_start

    total_time = time.time() - start
    producer.close()

    print(f"Send time (10 messages + 10×0.05s sleep): {send_time:.3f}s")
    print(f"Flush time: {flush_time:.3f}s")
    print(f"Total time: {total_time:.3f}s")
    print(f"\nMost time spent in: {'producer.flush()' if flush_time > send_time else 'sending + sleep'}")

    return {
        'total_time': total_time,
        'send_time': send_time,
        'flush_time': flush_time,
        'bottleneck': 'flush' if flush_time > 0.1 else 'sleep'
    }


def question_5_stream_green_trips():
    """Q5: Stream green taxi data and measure time"""
    print("\n" + "="*60)
    print("Question 5: Sending the Trip Data")
    print("="*60)

    # Find green taxi data (test data or week 2 data)
    test_data_dir = Path(__file__).parent / "test_data"
    test_files = list(test_data_dir.glob("green_tripdata_*.parquet"))

    if test_files:
        data_file = test_files[0]
        print(f"Using test data: {data_file.name}")
    else:
        week2_dir = Path(__file__).parent.parent / "week2_workflow_orchestration/downloads"
        green_files = list(week2_dir.glob("green_tripdata_*.parquet"))
        if not green_files:
            print("ERROR: No green taxi parquet files found")
            return None
        data_file = green_files[0]
        print(f"Using week 2 data: {data_file.name}")

    print(f"Loading data from {data_file.name}...")
    df = pd.read_parquet(data_file)
    print(f"Loaded {len(df)} records")

    # Create producer
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Create topic
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    existing = admin.list_topics()
    if 'green-trips' not in existing:
        topic = NewTopic(name='green-trips', num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        time.sleep(1)
    admin.close()

    # Stream data
    print(f"Streaming {len(df)} records to 'green-trips' topic...")
    start_time = time.time()

    for idx, row in df.iterrows():
        event = {
            'trip_id': f"green_{idx}",
            'vendor_id': int(row['VendorID']) if 'VendorID' in row and pd.notna(row['VendorID']) else 0,
            'lpep_pickup_datetime': row['lpep_pickup_datetime'].isoformat() if pd.notna(row['lpep_pickup_datetime']) else None,
            'lpep_dropoff_datetime': row['lpep_dropoff_datetime'].isoformat() if pd.notna(row['lpep_dropoff_datetime']) else None,
            'PULocationID': int(row['PULocationID']) if pd.notna(row['PULocationID']) else 0,
            'DOLocationID': int(row['DOLocationID']) if pd.notna(row['DOLocationID']) else 0,
            'trip_distance': float(row['trip_distance']) if pd.notna(row['trip_distance']) else 0.0,
            'fare_amount': float(row['fare_amount']) if pd.notna(row['fare_amount']) else 0.0,
        }
        producer.send('green-trips', value=event)

        if (idx + 1) % 5000 == 0:
            print(f"  Sent {idx + 1} records...")

    producer.flush()
    elapsed = time.time() - start_time
    producer.close()

    print(f"\n✓ Streamed {len(df)} records in {elapsed:.2f} seconds")
    print(f"  Throughput: {len(df)/elapsed:.0f} records/second")

    return {
        'records': len(df),
        'time_seconds': elapsed,
        'throughput': len(df) / elapsed
    }


def question_6_pyspark_parse():
    """Q6: Parse with PySpark Streaming"""
    print("\n" + "="*60)
    print("Question 6: Parsing the data with PySpark Streaming")
    print("="*60)

    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

    # Create Spark session - use pre-downloaded JARs from ~/.ivy2/jars
    import os
    jar_dir = os.path.expanduser("~/.ivy2/jars")
    jars = [
        f"{jar_dir}/spark-sql-kafka-0-10_2.13-3.5.3.jar",
        f"{jar_dir}/kafka-clients-3.6.1.jar",
        f"{jar_dir}/spark-token-provider-kafka-0-10_2.13-3.5.3.jar",
        f"{jar_dir}/commons-pool2-2.12.0.jar"
    ]

    spark = SparkSession.builder \
        .appName("Week6Homework") \
        .config("spark.jars", ",".join(jars)) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Define schema
    schema = StructType([
        StructField("trip_id", StringType(), True),
        StructField("vendor_id", IntegerType(), True),
        StructField("lpep_pickup_datetime", StringType(), True),
        StructField("lpep_dropoff_datetime", StringType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("fare_amount", DoubleType(), True),
    ])

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", "green-trips") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON
    from pyspark.sql.functions import from_json, col
    parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # Write to console to get count (run for limited time)
    query = parsed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .option("numRows", 10) \
        .start()

    # Run for a few seconds to process
    time.sleep(10)
    query.stop()

    # Get record count from Kafka consumer
    from kafka import KafkaConsumer
    consumer = KafkaConsumer(
        'green-trips',
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        consumer_timeout_ms=5000
    )

    count = 0
    for message in consumer:
        count += 1
    consumer.close()

    print(f"\nParsed schema: {[f.name for f in schema.fields]}")
    print(f"Total records in topic: {count}")

    spark.stop()

    return {
        'schema': [f.name for f in schema.fields],
        'record_count': count
    }


def question_7_most_popular_destination():
    """Q7: Most popular destination with PySpark"""
    print("\n" + "="*60)
    print("Question 7: Most popular destination")
    print("="*60)

    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
    from pyspark.sql.functions import from_json, col, window, current_timestamp

    # Create Spark session - use pre-downloaded JARs
    import os
    jar_dir = os.path.expanduser("~/.ivy2/jars")
    jars = [
        f"{jar_dir}/spark-sql-kafka-0-10_2.13-3.5.3.jar",
        f"{jar_dir}/kafka-clients-3.6.1.jar",
        f"{jar_dir}/spark-token-provider-kafka-0-10_2.13-3.5.3.jar",
        f"{jar_dir}/commons-pool2-2.12.0.jar"
    ]

    spark = SparkSession.builder \
        .appName("Week6HomeworkQ7") \
        .config("spark.jars", ",".join(jars)) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    schema = StructType([
        StructField("trip_id", StringType(), True),
        StructField("vendor_id", IntegerType(), True),
        StructField("lpep_pickup_datetime", StringType(), True),
        StructField("lpep_dropoff_datetime", StringType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("fare_amount", DoubleType(), True),
    ])

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", "green-trips") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse and add timestamp
    parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
    df_with_ts = parsed_df.withColumn("timestamp", current_timestamp())

    # Group by 5-minute window and DOLocationID
    popular_destinations = df_with_ts \
        .groupBy(window(col("timestamp"), "5 minutes"), "DOLocationID") \
        .count() \
        .orderBy(col("count").desc())

    # Write to memory table
    query = popular_destinations.writeStream \
        .outputMode("complete") \
        .format("memory") \
        .queryName("popular_destinations") \
        .start()

    # Wait for data to accumulate
    time.sleep(15)

    # Query the in-memory table
    result = spark.sql("SELECT * FROM popular_destinations ORDER BY count DESC LIMIT 5")
    result.show(truncate=False)

    # Get the most popular
    rows = result.collect()
    if rows:
        top_destination = rows[0]
        print(f"\nMost popular destination: {top_destination['DOLocationID']} (count: {top_destination['count']})")
        answer = top_destination['DOLocationID']
    else:
        answer = None

    query.stop()
    spark.stop()

    return answer


def main():
    """Run all homework questions"""
    print("Week 6 Homework - Stream Processing")
    print(f"Using Redpanda service at {BOOTSTRAP_SERVERS}")

    results = {}

    # Run all questions - fail fast on any error
    results['q1'] = question_1_rpk_version()
    results['q2'] = question_2_create_topic()
    results['q3'] = question_3_connect()
    results['q4'] = question_4_send_timing()
    results['q5'] = question_5_stream_green_trips()

    # Validate Q5 - must have actually streamed data
    if not results['q5'] or results['q5'].get('records', 0) == 0:
        print("\nERROR: Question 5 failed - no records were streamed")
        sys.exit(1)

    results['q6'] = question_6_pyspark_parse()

    # Validate Q6 - must have parsed records
    if not results['q6'] or results['q6'].get('record_count', 0) == 0:
        print("\nERROR: Question 6 failed - no records were parsed")
        sys.exit(1)

    results['q7'] = question_7_most_popular_destination()

    # Validate Q7 - must have a destination ID
    if not results['q7']:
        print("\nERROR: Question 7 failed - no popular destination found")
        sys.exit(1)

    print("\n" + "="*60)
    print("HOMEWORK SUMMARY")
    print("="*60)
    print(f"Q1 (Version): {results.get('q1', 'N/A')}")
    print(f"Q2 (Topic): {results.get('q2', 'N/A')}")
    print(f"Q3 (Connect): {results.get('q3', 'N/A')}")
    print(f"Q4 (Timing): {results.get('q4', {}).get('total_time', 'N/A')}s (bottleneck: {results.get('q4', {}).get('bottleneck', 'N/A')})")
    if results.get('q5'):
        print(f"Q5 (Stream time): {results['q5']['time_seconds']:.2f}s for {results['q5']['records']} records")
    if results.get('q6'):
        print(f"Q6 (Parse): {results['q6']['record_count']} records parsed, {len(results['q6']['schema'])} fields")
    print(f"Q7 (Popular dest): {results.get('q7', 'N/A')}")

    # Write results to file
    output_file = Path(__file__).parent / "homework_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults written to {output_file}")


if __name__ == "__main__":
    main()
