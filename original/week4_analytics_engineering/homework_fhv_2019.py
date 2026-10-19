"""
Week 4 Homework - FHV 2019
Official 2024 Cohort Questions

Using dbt + DuckDB for analytics engineering.
"""
import duckdb
import os

# Change to taxi_analytics directory where dbt ran
os.chdir('taxi_analytics')

# Connect to the DuckDB database created by dbt
con = duckdb.connect('taxi.duckdb')

print("=== Question 1: What is the count of records in stg_fhv_tripdata (2019)? ===")
q1 = con.execute("SELECT COUNT(*) FROM analytics.stg_fhv_tripdata").fetchone()
print(f"Answer: {q1[0]:,}")

print("\n=== Question 2: Distinct dispatching_base_num in fact_fhv_trips ===")
q2 = con.execute("SELECT COUNT(DISTINCT dispatching_base_num) FROM analytics.fact_fhv_trips").fetchone()
print(f"Answer: {q2[0]:,}")

print("\n=== Question 3: Count records with both pickup_zone and dropoff_zone ===")
q3 = con.execute("""
    SELECT COUNT(*)
    FROM analytics.fact_fhv_trips
    WHERE pickup_zone IS NOT NULL AND dropoff_zone IS NOT NULL
""").fetchone()
print(f"Answer: {q3[0]:,}")

print("\n=== Question 4: Check if shared rides (SR_Flag) are properly tracked ===")
q4_total = con.execute("SELECT COUNT(*) FROM analytics.fact_fhv_trips").fetchone()[0]
q4_with_flag = con.execute("""
    SELECT COUNT(*)
    FROM analytics.fact_fhv_trips
    WHERE shared_ride_flag IS NOT NULL
""").fetchone()[0]
print(f"Total records: {q4_total:,}")
print(f"Records with SR_Flag: {q4_with_flag:,}")
print(f"Percentage: {(q4_with_flag/q4_total*100):.1f}%")

print("\n=== Question 5: Most common pickup zone ===")
q5 = con.execute("""
    SELECT
        pickup_zone,
        COUNT(*) AS trip_count
    FROM analytics.fact_fhv_trips
    GROUP BY pickup_zone
    ORDER BY trip_count DESC
    LIMIT 5
""").fetchall()
print("Top 5 pickup zones:")
for zone, count in q5:
    print(f"  {zone}: {count:,} trips")

con.close()
