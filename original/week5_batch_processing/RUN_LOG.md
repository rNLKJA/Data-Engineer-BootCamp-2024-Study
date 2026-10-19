Reading data from /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/downloads
Found 3 Parquet files
Loaded 4,666,630 rows
After filtering: 4,581,859 valid rows

Monthly Statistics:
 pickup_year  pickup_month  trip_count  total_revenue  avg_revenue  total_distance  avg_distance  avg_passengers
        2008            12           8          84.76        10.60           10.71          1.34            1.62
        2009             1          19         256.52        13.50           44.92          2.36            1.37
        2020            12          16         339.58        21.22           77.03          4.81            1.06
        2021             1     1343375    24418537.70        18.18      6330837.04          4.71            1.42
        2021             2     1346357    24668573.30        18.32      5859976.85          4.35            1.41
        2021             3     1892069    34914376.96        18.45      8423492.63          4.45            1.41
        2021             4           8         131.86        16.48           23.01          2.88            1.50
        2021             5           7          99.69        14.24           13.25          1.89            1.00

Writing partitioned output to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week5_batch_processing/output/taxi_processed
  Wrote 8 rows to year=2008/month=12
  Wrote 19 rows to year=2009/month=1
  Wrote 16 rows to year=2020/month=12
  Wrote 1,343,375 rows to year=2021/month=1
  Wrote 1,346,357 rows to year=2021/month=2
  Wrote 1,892,069 rows to year=2021/month=3
  Wrote 8 rows to year=2021/month=4
  Wrote 7 rows to year=2021/month=5

Batch processing complete!

=== Homework Answers ===
Q1 2021 Total Revenue: $84,001,487.96
January 2021 Trip Count: 1,343,375
March 2021 Average Distance: 4.45 miles
Highest Average Revenue: Month 3.0 ($18.45 per trip)

## Week 5 Homework - FHV October 2019

**Date**: October 2026
**Dataset**: FHV October 2019
**Source**: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz

### Execution

```bash
python homework_fhv_oct2019.py
```

### Results

**Question 1**: Spark version (not reproducible locally)
**Question 2**: ~6 MB average per partition file
**Question 3**: 62,610 trips on October 15th, 2019
**Question 4**: 631,152.50 hours (longest trip duration)
**Question 5**: Port 4040 (Spark UI)
**Question 6**: Jamaica Bay (least frequent pickup zone with 1 pickup)

Note: Used DuckDB instead of PySpark due to Java compatibility issues. SQL logic is identical.
