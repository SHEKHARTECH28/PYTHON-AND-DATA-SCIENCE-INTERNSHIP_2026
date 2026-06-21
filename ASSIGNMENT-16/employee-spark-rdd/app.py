from pyspark.sql import SparkSession
import os

# Create Spark Session
spark = SparkSession.builder \
    .appName("EmployeeRDDProcessing") \
    .getOrCreate()

sc = spark.sparkContext

# Read CSV file
rdd = sc.textFile("data/employees.csv")

# Remove header
header = rdd.first()
data = rdd.filter(lambda row: row != header)

# Convert data into tuples
employees = data.map(lambda x: x.split(",")) \
                .map(lambda x: (
                    int(x[0]),      # id
                    x[1],           # name
                    x[2],           # department
                    int(x[3])       # salary
                ))

# --------------------------------------------------
# 1. Sort Employees by Salary Descending
# --------------------------------------------------

print("\n==============================")
print("Employees Sorted By Salary")
print("==============================")

sorted_employees = employees.sortBy(
    lambda x: x[3],
    ascending=False
)

for emp in sorted_employees.collect():
    print(emp)

# --------------------------------------------------
# 2. Department Wise Salary Total
# --------------------------------------------------

print("\n==============================")
print("Department Wise Total Salary")
print("==============================")

dept_salary = employees.map(
    lambda x: (x[2], x[3])
).reduceByKey(
    lambda a, b: a + b
)

for dept in dept_salary.collect():
    print(dept)

# --------------------------------------------------
# 3. Top 3 Highest Paid Employees
# --------------------------------------------------

print("\n==============================")
print("Top 3 Highest Paid Employees")
print("==============================")

top3 = sorted_employees.take(3)

for emp in top3:
    print(emp)

# --------------------------------------------------
# Save Output
# --------------------------------------------------

os.makedirs("output", exist_ok=True)

output_file = "output/top3_employees.csv"

with open(output_file, "w") as f:
    f.write("id,name,department,salary\n")

    for emp in top3:
        f.write(
            f"{emp[0]},{emp[1]},{emp[2]},{emp[3]}\n"
        )

print(f"\nTop 3 employees saved to: {output_file}")

spark.stop()