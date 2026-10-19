"""
Week 5 Homework - FHV October 2019
Official 2024 Cohort Questions

Using DuckDB instead of PySpark due to Java compatibility issues.
The SQL logic translates directly to Spark SQL.
"""
import duckdb
import os

con = duckdb.connect()

print("=== Question 1: Spark version ===")
print("Note: Using DuckDB instead due to Java incompatibility")
print("In a proper Spark environment, spark.version would show 3.3.2 or similar")

print("\n=== Loading FHV October 2019 data ===")
# Load CSV with proper types
con.execute("""
    CREATE TABLE fhv AS
    SELECT
        dispatching_base_num,
        CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
        CAST(dropOff_datetime AS TIMESTAMP) AS dropOff_datetime,
        PUlocationID,
        DOlocationID,
        SR_Flag,
        Affiliated_base_number
    FROM read_csv_auto('data/fhv_tripdata_2019-10.csv', header=true)
""")

total_records = con.execute("SELECT COUNT(*) FROM fhv").fetchone()[0]
print(f"Total records: {total_records:,}")

print("\n=== Question 2: Average parquet file size after repartition ===")
print("Note: Repartition to 6 would create 6 parquet files")
print("With DuckDB, we'll save to parquet and estimate:")

# Save to parquet
con.execute("COPY fhv TO 'output/fhv_2019_10_single.parquet' (FORMAT PARQUET)")
single_size = os.path.getsize('output/fhv_2019_10_single.parquet') / (1024 * 1024)
estimated_per_partition = single_size / 6
print(f"Single file size: {single_size:.2f} MB")
print(f"Estimated per partition (÷6): {estimated_per_partition:.2f} MB")

print("\n=== Question 3: Count trips on October 15th, 2019 ===")
oct15_count = con.execute("""
    SELECT COUNT(*)
    FROM fhv
    WHERE CAST(pickup_datetime AS DATE) = '2019-10-15'
""").fetchone()[0]
print(f"Trips on October 15th: {oct15_count:,}")

print("\n=== Question 4: Longest trip duration in hours ===")
longest_trip = con.execute("""
    SELECT MAX(EPOCH(dropOff_datetime - pickup_datetime) / 3600.0) AS duration_hours
    FROM fhv
    WHERE dropOff_datetime IS NOT NULL AND pickup_datetime IS NOT NULL
""").fetchone()[0]
print(f"Longest trip duration: {longest_trip:.2f} hours")

print("\n=== Question 5: Spark UI port ===")
print("Answer: Spark UI runs on port 4040")

print("\n=== Question 6: Least frequent pickup location zone ===")
# Load zone lookup
con.execute("""
    CREATE TABLE zones AS
    SELECT * FROM read_csv_auto('data/taxi_zone_lookup.csv', header=true)
""")

# Find least frequent pickup zone
result = con.execute("""
    SELECT z.Zone, COUNT(*) as pickup_count
    FROM fhv f
    JOIN zones z ON f.PUlocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY pickup_count ASC
    LIMIT 5
""").fetchall()

print("Least frequent pickup zones:")
for zone, count in result:
    print(f"  {zone}: {count} pickups")

print(f"\nAnswer: {result[0][0]}")

con.close()
