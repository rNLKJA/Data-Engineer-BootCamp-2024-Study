# connect to postgres database
from sqlalchemy import create_engine
import pandas as pd
import argparse
from time import time


# read file path and table name from command line
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--file_path', '-f', type=str, help='The path to the file')
parser.add_argument('--table_name', '-t', type=str, help='The name of the table')

args = parser.parse_args()

file_path = args.file_path
table_name = args.table_name

# create database engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# define data loading iterator
df_iter = pd.read_csv(file_path, iterator=True, chunksize=100000, low_memory=False)

# init a empty table
df = next(df_iter)
df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
df.to_sql(name=table_name, con=engine, if_exists='append')

# insert data chunk by chunk
while True: 
    t_start = time()

    # avoid StopIteration error
    try:
        df = next(df_iter)
    except StopIteration:
        break

    # convert datetime columns to datetime type
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    # insert data chunk
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # print time
    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end - t_start))