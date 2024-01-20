from tqdm import tqdm
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os
from os.path import getsize
from urllib.request import urlretrieve
from pathlib import Path

def download_taxi_data(download_path, year, start_month, end_month):
    output_dir = download_path + f"/{year}_yellow_taxi_data"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    downloaded_files = []

    for m in tqdm(range(start_month, end_month + 1), desc="Downloading"):
        filename = f'yellow_tripdata_{year}-{str(m).zfill(2)}.parquet'
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{filename}"
        file_path = f"{output_dir}/{filename}"
        urlretrieve(url, file_path)
        print(f"Downloaded {filename} to {output_dir} with size {getsize(file_path) / 1073741824:.2f}GB")

        downloaded_files.append(file_path)

    return downloaded_files

def load_data_into_db(file_path, table_name, user, password, host, port, database):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    print(f"Loading data from {file_path} into table {table_name}...")
    df = pd.read_parquet(file_path)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    if_exists_param = 'replace' if table_name.endswith("_01") else 'append'
    df.to_sql(name=table_name, con=engine, if_exists=if_exists_param, index=False)
    
    print(f'Data from {file_path} loaded into {table_name}.')

parser = argparse.ArgumentParser(description='Load Parquet file into PostgreSQL database.')
parser.add_argument('--table_name', '-t', type=str, required=True, help='The base name of the table')
parser.add_argument('--user', type=str, required=True, help='The username for the PostgreSQL database')
parser.add_argument('--password', type=str, required=True, help='The password for the PostgreSQL database')
parser.add_argument('--host', type=str, required=True, help='The host address for the PostgreSQL database')
parser.add_argument('--port', type=int, required=True, help='The port number for the PostgreSQL database')
parser.add_argument('--database', type=str, required=True, help='The name of the PostgreSQL database')
parser.add_argument('--download_path', default='.', help='Path to download the data')
parser.add_argument('--year', '-y', type=int, default=2019, help='Year of the data')
parser.add_argument('--start_month', '-s', type=int, default=1, help='Start month (1-12)')
parser.add_argument('--end_month', '-e', type=int, default=12, help='End month (1-12)')

args = parser.parse_args()

if __name__ == "__main__":
    print('Starting the download process...')
    downloaded_files = download_taxi_data(args.download_path, args.year, args.start_month, args.end_month)

    for file_path in downloaded_files:
        month_str = Path(file_path).stem.split('-')[-1]  # Extract month from filename
        month_table_name = f"{args.table_name}_{args.year}_{month_str}"
        load_data_into_db(file_path, month_table_name, args.user, args.password, args.host, args.port, args.database)
    
    print('All data downloaded and loaded into the database.')
