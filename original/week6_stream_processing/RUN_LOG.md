# Week 6 Homework CI Run Log

CI Run: https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study/actions/runs/39251395979

Dataset: `green_tripdata_2019-10.csv.gz` (476,386 records from October 2019 NYC Green Taxi data)

## Question 5: Sending the Trip Data

```
✓ Streamed 476386 records in 28.90 seconds
  Throughput: 16482 records/second
```

The script downloaded the official dataset from:
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz

Each record contains these fields from the 2019-10 Green Taxi data:
- lpep_pickup_datetime
- lpep_dropoff_datetime
- PULocationID
- DOLocationID
- passenger_count
- trip_distance
- tip_amount

## Question 6: Parsing the data with PySpark Streaming

```
Parsed schema fields: ['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount']
Total records in topic: 476386
```

PySpark successfully parsed all 476,386 records using the homework schema:
- String fields: lpep_pickup_datetime, lpep_dropoff_datetime
- Integer fields: PULocationID, DOLocationID
- Double fields: passenger_count, trip_distance, tip_amount

## Question 7: Most popular destination

Streaming aggregation with 5-minute window on `current_timestamp()`:

```
Batch: 0
-------------------------------------------
+------------------------------------------+------------+-----+
|window                                    |DOLocationID|count|
+------------------------------------------+------------+-----+
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|74          |17741|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|42          |15942|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|41          |14061|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|75          |12840|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|129         |11930|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|7           |11533|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|166         |10845|
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|236         |7913 |
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|223         |7542 |
|{2026-10-19 12:20:00, 2026-10-19 12:25:00}|238         |7318 |
+------------------------------------------+------------+-----+
only showing top 10 rows

Most popular destination: DOLocationID 74 with 17741 trips
```

**Answer**: DOLocationID **74**

The homework uses `current_timestamp()` for windowing, which creates windows based on when records are processed (2026-10-19), not when the original trips occurred (2019-10). This is as specified in the official homework instructions.

## Notes

All three questions (Q5, Q6, Q7) use the real October 2019 Green Taxi dataset with 476,386 records, matching the official 2024 Data Engineering Zoomcamp homework requirements.
