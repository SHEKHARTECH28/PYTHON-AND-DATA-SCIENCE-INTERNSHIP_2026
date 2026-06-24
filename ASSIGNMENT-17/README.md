# PySpark Sales Analysis

## Objective
Analyze sales data using PySpark DataFrames.

## Operations Performed

1. Read CSV file into DataFrame
2. Sort products by sales in descending order
3. Display top 3 products by sales
4. Filter products with sales > 80,000
5. Save filtered output as CSV

## Build Docker Image

```bash
docker build -t sales-pyspark .
```

## Run Docker Container

```bash
docker run --rm -v ${PWD}/output:/app/output sales-pyspark
```

## Technologies Used

- Python 3.12
- Apache Spark (PySpark)
- Docker
- Java 17