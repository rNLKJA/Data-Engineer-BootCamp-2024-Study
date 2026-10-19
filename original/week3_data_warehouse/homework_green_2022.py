"""
Week 3 Homework - Green Taxi 2022
Official 2024 Cohort Questions

Using DuckDB as local substitute for BigQuery.
Dataset: Green taxi 2022 parquet files
"""
import duckdb
import requests
from pathlib import Path

# Download green taxi 2022 parquet files
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
year = 2022
data_dir = Path("data/green_2022")
data_dir.mkdir(parents=True, exist_ok=True)

print("Downloading green taxi 2022 parquet files...")
for month in range(1, 13):
    filename = f"green_tripdata_{year}-{month:02d}.parquet"
    filepath = data_dir / filename
    
    if not filepath.exists():
        url = base_url + filename
        print(f"  {filename}...")
        response = requests.get(url)
        if response.status_code == 200:
            filepath.write_bytes(response.content)
        else:
            print(f"    Failed: {response.status_code}")

# Connect to DuckDB
con = duckdb.connect(':memory:')

# Create external table (reading from parquet files)
print("\nCreating external table...")
con.execute("""
    CREATE VIEW green_taxi_external AS 
    SELECT * FROM read_parquet('data/green_2022/*.parquet')
""")

# Create materialized table (actual table in DuckDB)
print("Creating materialized table...")
con.execute("""
    CREATE TABLE green_taxi_materialized AS 
    SELECT * FROM green_taxi_external
""")

print("\n=== Question 1: Count of records for 2022 Green Taxi Data ===")
count_result = con.execute("SELECT COUNT(*) FROM green_taxi_materialized").fetchone()
print(f"Total records: {count_result[0]:,}")

print("\n=== Question 2: Distinct PULocationIDs ===")
print("Note: BigQuery estimates data to be read. DuckDB doesn't show estimates the same way.")
print("External table (reading from parquet):")
distinct_ext = con.execute("SELECT COUNT(DISTINCT PULocationID) FROM green_taxi_external").fetchone()
print(f"  Distinct PULocationIDs: {distinct_ext[0]}")

print("Materialized table (in-memory table):")
distinct_mat = con.execute("SELECT COUNT(DISTINCT PULocationID) FROM green_taxi_materialized").fetchone()
print(f"  Distinct PULocationIDs: {distinct_mat[0]}")
print("  (DuckDB local equivalent - actual storage scanning behavior differs from BigQuery)")

print("\n=== Question 3: Records with fare_amount = 0 ===")
zero_fare = con.execute("SELECT COUNT(*) FROM green_taxi_materialized WHERE fare_amount = 0").fetchone()
print(f"Records with fare_amount = 0: {zero_fare[0]:,}")

print("\n=== Question 4: Best strategy for optimization ===")
print("For queries that ORDER BY PULocationID and filter by lpep_pickup_datetime:")
print("Answer: Partition by lpep_pickup_datetime, Cluster on PULocationID")
print("\nCreating optimized table...")
con.execute("""
    CREATE TABLE green_taxi_optimized AS 
    SELECT * FROM green_taxi_materialized 
    ORDER BY lpep_pickup_datetime, PULocationID
""")

print("\n=== Question 5: Query distinct PULocationID for June 2022 ===")
print("Non-partitioned table:")
june_result_mat = con.execute("""
    SELECT COUNT(DISTINCT PULocationID) 
    FROM green_taxi_materialized 
    WHERE lpep_pickup_datetime >= '2022-06-01' 
      AND lpep_pickup_datetime < '2022-07-01'
""").fetchone()
print(f"  Distinct locations: {june_result_mat[0]}")

print("Optimized (sorted) table:")
june_result_opt = con.execute("""
    SELECT COUNT(DISTINCT PULocationID) 
    FROM green_taxi_optimized 
    WHERE lpep_pickup_datetime >= '2022-06-01' 
      AND lpep_pickup_datetime < '2022-07-01'
""").fetchone()
print(f"  Distinct locations: {june_result_opt[0]}")
print("  (DuckDB local equivalent - BigQuery shows MB to scan, DuckDB processes differently)")

print("\n=== Question 6: Where is data stored in External Table? ===")
print("Answer: GCP Bucket (in BigQuery context)")
print("Note: In our DuckDB setup, data is stored in local parquet files")

print("\n=== Question 7: Is it best practice to always cluster data in BigQuery? ===")
print("Answer: False")
print("Clustering is beneficial for large tables with high-cardinality columns that are")
print("frequently used in filters. For small tables or columns with few distinct values,")
print("clustering adds overhead without performance benefit.")

print("\n=== Question 8 (Bonus): SELECT count(*) bytes estimate ===")
count_all = con.execute("SELECT COUNT(*) FROM green_taxi_materialized").fetchone()
print(f"Count result: {count_all[0]:,}")
print("Why small estimate: BigQuery knows table metadata (row count) without scanning data.")
print("COUNT(*) only needs metadata, not the actual data columns, so bytes scanned ≈ 0.")

con.close()
