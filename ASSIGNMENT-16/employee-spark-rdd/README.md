# Employee Salary Analysis using PySpark RDD

## Objective

Process employee data using PySpark RDDs.

### Operations

1. Read CSV using RDD.
2. Sort employees by salary descending.
3. Calculate department-wise total salary.
4. Find top 3 highest-paid employees.
5. Save top 3 employees to output file.

---

## Dataset

employees.csv

```csv
id,name,department,salary
1,Amit,IT,55000
2,Rahul,HR,40000
3,Neha,IT,65000
4,Priya,Finance,70000
5,Karan,IT,50000
6,Simran,HR,45000
7,Rohit,Finance,60000
```

## Build Docker Image

```bash
docker build -t employee-spark .
```

## Run Container

```bash
docker run --rm employee-spark
```

## Output

- Sorted employees by salary
- Department salary totals
- Top 3 employees saved in:

```text
output/top3_employees
```