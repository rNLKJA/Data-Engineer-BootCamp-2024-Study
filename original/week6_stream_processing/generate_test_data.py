#!/usr/bin/env python3
"""
Generate a small synthetic green taxi dataset for Week 6 homework testing.
This is NOT real NYC TLC data, but follows the schema for CI testing.
"""
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_test_data(num_records=100):
    """Generate synthetic green taxi records"""
    random.seed(42)
    base_time = datetime(2024, 1, 15, 8, 0, 0)

    records = []
    for i in range(num_records):
        pickup_time = base_time + timedelta(minutes=i*5)
        trip_duration_mins = random.randint(5, 45)
        dropoff_time = pickup_time + timedelta(minutes=trip_duration_mins)
        trip_distance = round(random.uniform(0.5, 15.0), 2)

        record = {
            'VendorID': random.choice([1, 2]),
            'lpep_pickup_datetime': pickup_time,
            'lpep_dropoff_datetime': dropoff_time,
            'store_and_fwd_flag': random.choice(['N', 'Y']),
            'RatecodeID': random.choice([1, 1, 1, 1, 2]),  # mostly standard rate
            'PULocationID': random.randint(1, 265),
            'DOLocationID': random.randint(1, 265),
            'passenger_count': random.choice([1, 1, 1, 2, 2, 3]),
            'trip_distance': trip_distance,
            'fare_amount': round(2.5 + trip_distance * 2.5, 2),
            'extra': round(random.choice([0, 0, 0.5, 1.0]), 2),
            'mta_tax': 0.5,
            'tip_amount': round(random.uniform(0, 5.0), 2),
            'tolls_amount': round(random.choice([0, 0, 0, 0, 2.75, 5.76]), 2),
            'ehail_fee': None,
            'improvement_surcharge': 0.3,
            'total_amount': 0.0,  # will calculate
            'payment_type': random.choice([1, 1, 1, 2]),
            'trip_type': 1,
            'congestion_surcharge': round(random.choice([0, 2.5]), 2)
        }

        # Calculate total
        record['total_amount'] = round(
            record['fare_amount'] + record['extra'] + record['mta_tax'] +
            record['tip_amount'] + record['tolls_amount'] +
            record['improvement_surcharge'] + record['congestion_surcharge'], 2
        )

        records.append(record)

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = generate_test_data(100)
    output_file = "test_data/green_tripdata_test.parquet"

    import os
    os.makedirs("test_data", exist_ok=True)
    df.to_parquet(output_file, index=False)

    print(f"Generated {len(df)} synthetic green taxi records")
    print(f"Saved to: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")
    print("\nFirst record:")
    print(df.iloc[0].to_dict())
