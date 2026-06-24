from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create Spark Session
spark = SparkSession.builder \
    .appName("SalesAnalysis") \
    .getOrCreate()

# Read CSV File
df = spark.read.csv(
    "data/sales.csv",
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL DATA ==========")
df.show()

# Sort products by sales descending
print("\n========== SORTED BY SALES DESC ==========")
sorted_df = df.orderBy(col("sales").desc())
sorted_df.show()

# Top 3 products with highest sales
print("\n========== TOP 3 PRODUCTS ==========")
top3_df = sorted_df.limit(3)
top3_df.show()

# Filter products with sales > 80000
print("\n========== SALES > 80000 ==========")
high_sales_df = df.filter(col("sales") > 80000)
high_sales_df.show()

# Save output to CSV
high_sales_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("output/high_sales_products")

print("\nOutput saved in output/high_sales_products")

spark.stop()