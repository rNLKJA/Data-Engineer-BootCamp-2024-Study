
from tqdm import tqdm  # for progress bar
import pandas as pd
from sqlalchemy import create_engine
import argparse

# read file path and table name from command line
parser = argparse.ArgumentParser(description='Load Parquet file into PostgreSQL database.')
parser.add_argument('--file_path', '-f', type=str, help='The path to the file')
parser.add_argument('--table_name', '-t', type=str, help='The name of the table')

args = parser.parse_args()

file_path = args.file_path
table_name = args.table_name

# create database engine
print("Creating database engine...")
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# read the entire Parquet file into a DataFrame
print(f"Reading Parquet file: {file_path}")
df = pd.read_parquet(file_path)



# Convert datetime columns to datetime type
print("Converting datetime columns...")
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# Optionally, visualize data here using Matplotlib or Seaborn

# Load data into PostgreSQL
print("Loading data into PostgreSQL...")
df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

print('Data loading completed.')
