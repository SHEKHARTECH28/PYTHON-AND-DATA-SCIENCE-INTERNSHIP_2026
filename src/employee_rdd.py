from pyspark import SparkConf, SparkContext
import os

def main():

    # Spark configuration
    conf = SparkConf().setAppName("EmployeeRDDProcessing").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # Input CSV file path (inside Docker)
    input_file = "/app/data/employees.csv"

    # Read CSV into RDD
    rdd = sc.textFile(input_file)

    # Extract header
    header = rdd.first()

    # Convert CSV → structured RDD
    employee_rdd = (
        rdd.filter(lambda row: row != header)
           .map(lambda row: row.split(","))
           .map(lambda x: {
               "id": int(x[0]),
               "name": x[1],
               "department": x[2],
               "salary": int(x[3])
           })
    )

    # ----------------------------
    # 1. SORT BY SALARY (DESC)
    # ----------------------------
    print("\n=== Employees Sorted by Salary ===")

    sorted_employees = employee_rdd.sortBy(lambda x: x["salary"], ascending=False)

    for emp in sorted_employees.collect():
        print(emp)

    # ----------------------------
    # 2. DEPARTMENT TOTAL SALARY
    # ----------------------------
    print("\n=== Department-wise Total Salary ===")

    dept_salary = (
        employee_rdd
        .map(lambda x: (x["department"], x["salary"]))
        .reduceByKey(lambda a, b: a + b)
    )

    for dept, total in dept_salary.collect():
        print((dept, total))

    # ----------------------------
    # 3. TOP 3 EMPLOYEES
    # ----------------------------
    print("\n=== Top 3 Highest Paid Employees ===")

    top3 = sorted_employees.take(3)

    for emp in top3:
        print(emp)

    # ----------------------------
    # 4. SAVE OUTPUT (SAFE FIX)
    # ----------------------------
    os.makedirs("/app/output", exist_ok=True)

    output_file = "/app/output/top3.txt"

    with open(output_file, "w") as f:
        for e in top3:
            f.write(f"{e['id']},{e['name']},{e['department']},{e['salary']}\n")

    sc.stop()


if __name__ == "__main__":
    main()