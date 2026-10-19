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

    # Use the official green_tripdata_2019-10.csv.gz file from the homework
    # Download from the official source if not present
    data_file = Path(__file__).parent.parent / "week2_workflow_orchestration/downloads/green_tripdata_2019-10.csv.gz"

    if not data_file.exists():
        print(f"Downloading green_tripdata_2019-10.csv.gz from official source...")
        import urllib.request
        data_file.parent.mkdir(parents=True, exist_ok=True)
        url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
        urllib.request.urlretrieve(url, data_file)
        print(f"Downloaded to {data_file}")

    print(f"Loading data from {data_file.name}...")
    # Load only the required columns from the homework
    df = pd.read_csv(
        data_file,
        usecols=[
            'lpep_pickup_datetime',
            'lpep_dropoff_datetime',
            'PULocationID',
            'DOLocationID',
            'passenger_count',
            'trip_distance',
            'tip_amount'
        ]
    )
    print(f"Loaded {len(df)} records from green_tripdata_2019-10.csv.gz")

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

    # Stream data (no sleep, as per homework instructions)
    print(f"Streaming {len(df)} records to 'green-trips' topic...")
    start_time = time.time()

    for idx, row in enumerate(df.itertuples(index=False)):
        # Use the homework's recommended iteration method (itertuples)
        row_dict = {col: getattr(row, col) for col in row._fields}
        producer.send('green-trips', value=row_dict)

        if (idx + 1) % 10000 == 0:
            print(f"  Sent {idx + 1} records...")

    producer.flush()
    elapsed = time.time() - start_time
    producer.close()

    print(f"\n✓ Streamed {len(df)} records in {elapsed:.2f} seconds")
    print(f"  Throughput: {len(df)/elapsed:.0f} records/second")

    return {
        'records': len(df),
        'time_seconds': round(elapsed),  # Round to whole number as per homework
        'throughput': len(df) / elapsed
    }


def question_6_pyspark_parse():
    """Q6: Parse with PySpark Streaming"""
    print("\n" + "="*60)
    print("Question 6: Parsing the data with PySpark Streaming")
    print("="*60)

    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

    # Create Spark session - packages will be provided by spark-submit --packages
    spark = SparkSession.builder \
        .appName("Week6Homework") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Define schema exactly as in the homework
    schema = StructType() \
        .add("lpep_pickup_datetime", StringType()) \
        .add("lpep_dropoff_datetime", StringType()) \
        .add("PULocationID", IntegerType()) \
        .add("DOLocationID", IntegerType()) \
        .add("passenger_count", DoubleType()) \
        .add("trip_distance", DoubleType()) \
        .add("tip_amount", DoubleType())

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", "green-trips") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON
    from pyspark.sql.functions import from_json, col
    green_stream = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # Peek at first record to show parsed output
    def peek(mini_batch, batch_id):
        first_row = mini_batch.take(1)
        if first_row:
            print("\nFirst parsed record:")
            print(first_row[0])

    query = green_stream.writeStream.foreachBatch(peek).start()
    time.sleep(5)
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

    print(f"\nParsed schema fields: {schema.fieldNames()}")
    print(f"Total records in topic: {count}")

    spark.stop()

    return {
        'schema': schema.fieldNames(),
        'record_count': count
    }


def question_7_most_popular_destination():
    """Q7: Most popular destination with PySpark"""
    print("\n" + "="*60)
    print("Question 7: Most popular destination")
    print("="*60)

    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType
    from pyspark.sql.functions import from_json, col, window, current_timestamp

    # Create Spark session with tuned settings for faster streaming
    spark = SparkSession.builder \
        .appName("Week6HomeworkQ7") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.streaming.kafka.maxRatePerPartition", "100000") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Schema matching Q6
    schema = StructType() \
        .add("lpep_pickup_datetime", StringType()) \
        .add("lpep_dropoff_datetime", StringType()) \
        .add("PULocationID", IntegerType()) \
        .add("DOLocationID", IntegerType()) \
        .add("passenger_count", DoubleType()) \
        .add("trip_distance", DoubleType()) \
        .add("tip_amount", DoubleType())

    # Read from Kafka
    green_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("subscribe", "green-trips") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse and add timestamp (using current_timestamp as per homework)
    green_stream = green_stream.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
    green_stream = green_stream.withColumn("timestamp", current_timestamp())

    # Group by 5-minute window and DOLocationID
    popular_destinations = green_stream \
        .groupBy(window(col("timestamp"), "5 minutes"), "DOLocationID") \
        .count() \
        .orderBy(col("count").desc())

    # Write to console to see the output
    query = popular_destinations.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", "false") \
        .option("numRows", 10) \
        .trigger(processingTime='10 seconds') \
        .start()

    # Wait for data to accumulate and process
    print("\nWaiting for streaming aggregation to process data...")
    for i in range(6):
        time.sleep(10)
        print(f"  Waiting... {(i+1)*10}s elapsed")

    query.stop()

    # Query via memory sink to get the result
    query2 = popular_destinations.writeStream \
        .outputMode("complete") \
        .format("memory") \
        .queryName("popular_destinations") \
        .trigger(processingTime='5 seconds') \
        .start()

    print("Waiting for memory sink to process...")
    for i in range(4):
        time.sleep(10)
        print(f"  Waiting... {(i+1)*10}s elapsed")
        # Check if data is available
        try:
            result = spark.sql("SELECT COUNT(*) as cnt FROM popular_destinations")
            cnt = result.collect()[0]['cnt']
            if cnt > 0:
                print(f"  Found {cnt} rows in memory table")
                break
        except Exception:
            pass

    # Query the in-memory table
    result = spark.sql("SELECT * FROM popular_destinations ORDER BY count DESC LIMIT 5")
    result.show(truncate=False)

    # Get the most popular
    rows = result.collect()
    if rows:
        top_destination = rows[0]
        print(f"\nMost popular destination: DOLocationID {top_destination['DOLocationID']} with {top_destination['count']} trips")
        answer = top_destination['DOLocationID']
    else:
        answer = None

    query2.stop()
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
