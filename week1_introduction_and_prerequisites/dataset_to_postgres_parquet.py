from tqdm import tqdm  # for progress bar
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os
from os.path import getsize

import pandas as pd
from sqlalchemy import create_engine
import argparse

from os.path import getsize
from urllib.request import urlretrieve
from pathlib import Path

# Global parameter
append = False

def download_taxi_data(download_path, year, start_month, end_month):
    # specify the output directory
    output_dir = download_path + f"/{year}_yellow_taxi_data"

    # create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # obtain data from Jan to Dec
    for m in tqdm(range(start_month, end_month+1), desc="Downloading"):
        out = f'yellow_tripdata_{year}-{str(m).zfill(2)}.parquet'
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{out}"
        urlretrieve(url, f"{output_dir}/{out}")
        print(f"Done downloading {out} to {output_dir} with size {getsize(f'{output_dir}/{out}') / 1073741824:.2f}GB")

        # Load data into PostgreSQL
        print(f"Loading {out} into PostgreSQL...")
        file_path = f"{output_dir}/{out}"
        main(file_path=file_path, table_name=args.table_name, user=args.user, password=args.password, host=args.host, port=args.port, database=args.database, url=args.url)


def main(file_path, table_name, user, password, host, port, database, url):
    global append  # Use the global append parameter

    # create database engine
    print("Creating database engine...")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    
    # read the entire Parquet file into a DataFrame
    print(f"Reading Parquet file: {file_path}")
    df = pd.read_parquet(file_path)

    # Convert datetime columns to datetime type
    print("Converting datetime columns...")
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Appending mode check
    if append == False:
        # init a empty table
        print("Initializing a empty table...")
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Load data into PostgreSQL
    print("Loading data into PostgreSQL...")
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    
    append = True  # Change the append parameter to True after the first execution

    print('Data loading completed.')

# read file path and table name from command line
parser = argparse.ArgumentParser(description='Load Parquet file into PostgreSQL database.')
# parser.add_argument('--file_path', '-f', type=str, help='The path to the file')
parser.add_argument('--table_name', '-t', type=str, help='The name of the table')
parser.add_argument('--user', type=str, help='The username for the PostgreSQL database')
parser.add_argument('--password', type=str, help='The password for the PostgreSQL database')
parser.add_argument('--host', type=str, help='The host address for the PostgreSQL database')
parser.add_argument('--port', type=int, help='The port number for the PostgreSQL database')
parser.add_argument('--database', type=str, help='The name of the PostgreSQL database')
parser.add_argument('--url', type=str, help='The URL for the PostgreSQL database')
parser.add_argument('--download_path', default='.', help='Path to download the data')
parser.add_argument('--year', '-y', type=int, default=2019, help='Year of the data')
parser.add_argument('--start_month', '-s', type=int, default=1, help='Start month (1-12)')
parser.add_argument('--end_month', '-e', type=int, default=12, help='End month (1-12)')

args = parser.parse_args()

download_params = {
    'download_path': args.download_path,
    'year': args.year,
    'start_month': args.start_month,
    'end_month': args.end_month
}

main_params = {
    # 'file_path': args.file_path,
    'table_name': args.table_name,
    'user': args.user,
    'password': args.password,
    'host': args.host,
    'port': args.port,
    'database': args.database,
    'url': args.url
}



if __name__ == "__main__":
    print('start downloading...')
    download_taxi_data(**download_params)

    my_download_file_paths = list(Path(download_params['download_path']).iterdir())

    
    print('display downloaded content')    


    # Execute main() function for each file
    for file_path in my_download_file_paths:
        print(f'working on file {file_path}')
        main(file_path=file_path, **main_params)
