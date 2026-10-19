"""
Week 2 Homework - Green Taxi ETL Pipeline
Official 2024 Cohort Questions
"""
import pandas as pd
import requests
from pathlib import Path

# Download green taxi data for Q4 2020 (Oct, Nov, Dec)
base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/"
months = [10, 11, 12]
year = 2020

downloads_dir = Path("downloads/green")
downloads_dir.mkdir(parents=True, exist_ok=True)

dfs = []
for month in months:
    filename = f"green_tripdata_{year}-{month:02d}.csv.gz"
    filepath = downloads_dir / filename
    
    if not filepath.exists():
        url = base_url + filename
        print(f"Downloading {filename}...")
        response = requests.get(url)
        filepath.write_bytes(response.content)
    
    print(f"Reading {filename}...")
    df = pd.read_csv(filepath, compression='gzip', parse_dates=['lpep_pickup_datetime', 'lpep_dropoff_datetime'])
    dfs.append(df)

# Concatenate all three months
df_green = pd.concat(dfs, ignore_index=True)

print("\n=== Question 1: Data Loading ===")
print(f"Dataset shape: {df_green.shape[0]:,} rows x {df_green.shape[1]} columns")
print(f"Answer: {df_green.shape[0]:,} rows x {df_green.shape[1]} columns")

print("\n=== Question 2: Data Transformation ===")
print("Filtering where passenger_count > 0 AND trip_distance > 0")
df_filtered = df_green[(df_green['passenger_count'] > 0) & (df_green['trip_distance'] > 0)]
print(f"Rows after filtering: {len(df_filtered):,}")

print("\n=== Question 3: Data Transformation ===")
print("Creating lpep_pickup_date column:")
print("Correct method: data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date")
df_green['lpep_pickup_date'] = df_green['lpep_pickup_datetime'].dt.date
print(f"Sample: {df_green['lpep_pickup_date'].head()}")

print("\n=== Question 4: Data Transformation ===")
print("Existing VendorID values:")
vendor_ids = sorted(df_green['VendorID'].dropna().unique())
print(f"VendorID values: {vendor_ids}")

print("\n=== Question 5: Data Transformation ===")
print("Columns that need snake_case renaming:")
camel_case_cols = [col for col in df_green.columns if col != col.lower() or col != col.replace(' ', '_')]
print(f"Columns to rename: {camel_case_cols}")
print(f"Count: {len(camel_case_cols)}")

print("\n=== Question 6: Data Exporting ===")
print("Number of unique pickup dates (partitions):")
unique_dates = df_green['lpep_pickup_date'].nunique()
print(f"Unique dates: {unique_dates}")
print("This is the number of parquet partitions (folders) when partitioned by lpep_pickup_date")
