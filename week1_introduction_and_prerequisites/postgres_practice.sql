SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
 	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pickup_loc",
 	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_trip_2021_01 AS t 
JOIN zones AS zpu ON t."PULocationID" = zpu."LocationID"
JOIN zones AS zdo ON t."PULocationID" = zdo."LocationID"

LIMIT 100;

SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_trip_2021_01 AS t 
WHERE	
	"PULocationID" IS NULL OR
	"DOLocationID" IS NULL
LIMIT 100;



SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_trip_2021_01 AS t 
WHERE	
	"PULocationID" NOT IN (
		SELECT 
			"LocationID" 
		FROM 
			zones
	) OR
	"DOLocationID" NOT IN (
		SELECT 
			"LocationID" 
		FROM 
			zones
	)
LIMIT 100;



SELECT 
-- 	DATE_TRUNC('DAY', tpep_dropoff_datetime)
	CAST (tpep_dropoff_datetime AS DATE) AS "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount),
	MAX(passenger_count)
FROM 
	yellow_taxi_trip_2021_01 AS t 
GROUP BY
	CAST(tpep_dropoff_datetime AS date), "DOLocationID"
ORDER BY "day" DESC;
-- LIMIT 100;

