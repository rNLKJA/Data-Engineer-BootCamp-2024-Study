import os
from os.path import getsize
from urllib.request import urlretrieve
import argparse
from tqdm import tqdm

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NYC Yellow Taxi Data Downloader')
    parser.add_argument('--download_path', default='.', help='Path to download the data')
    parser.add_argument('--year', '-y', type=int, default=2019, help='Year of the data')
    parser.add_argument('--start_month', '-s', type=int, default=1, help='Start month (1-12)')
    parser.add_argument('--end_month', '-e', type=int, default=12, help='End month (1-12)')
    args = parser.parse_args()

    download_taxi_data(args.download_path, args.year, args.start_month, args.end_month)
    


