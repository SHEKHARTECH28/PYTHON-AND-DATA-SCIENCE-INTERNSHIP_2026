CREATE DATABASE data_bank;
USE data_bank;


CREATE SCHEMA data_bank;




CREATE TABLE regions (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50)
);

CREATE TABLE customer_nodes (
    customer_id INT,
    region_id INT,
    node_id INT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE customer_transactions (
    customer_id INT,
    txn_date DATE,
    txn_type VARCHAR(20),
    txn_amount INT
);
 ------------------------------A. Customer Nodes Exploration----------------------------------------------


  --1 How many unique nodes are there on the Data Bank system?
  select  count(distinct node_id) as unique_node from customer_nodes;

  --2What is the number of nodes per region?
    select region_id, count(  node_id) as total from customer_nodes 
     group by region_id ;

--3How many customers are allocated to each region?
select  region_id ,count( distinct customer_id)  as Total_customer from customer_nodes
group by region_id;

--4 How many days on average are customers reallocated to a different node?
SELECT
    AVG(DATEDIFF(day, start_date, end_date)) AS avg_days
FROM customer_nodes
WHERE end_date <> '9999-12-31';

--5What is the median, 80th and 95th percentile for this same reallocation days metric for each region?

SELECT DISTINCT
    r.region_name,

    PERCENTILE_CONT(0.5)
    WITHIN GROUP (
        ORDER BY DATEDIFF(DAY, c.start_date, c.end_date)
    ) OVER (PARTITION BY c.region_id) AS median,

    PERCENTILE_CONT(0.8)
    WITHIN GROUP (
        ORDER BY DATEDIFF(DAY, c.start_date, c.end_date)
    ) OVER (PARTITION BY c.region_id) AS percentile_80,

    PERCENTILE_CONT(0.95)
    WITHIN GROUP (
        ORDER BY DATEDIFF(DAY, c.start_date, c.end_date)
    ) OVER (PARTITION BY c.region_id) AS percentile_95

FROM customer_nodes c
JOIN regions r
    ON c.region_id = r.region_id
WHERE c.end_date <> '9999-12-31';


------------------------------------------------B. Customer Transactions---------------------------------------

--1What is the unique count and total amount for each transaction type?
SELECT
    txn_type,
    COUNT(*) AS transaction_count,
    SUM(txn_amount) AS total_amount
FROM customer_transactions
GROUP BY txn_type;

--2 What is the average total historical deposit counts and amounts for all customers?
select avg(deposit_count) as average_count , avg(deposit_amount) as average_amount from 
(
select customer_id , count(*) as deposit_count ,sum(txn_amount) as
deposit_amount from customer_transactions
where txn_type='deposit' group by customer_id ) d  ;

--3For each month - how many Data Bank customers make more than 1 deposit and either 1 purchase or 1 withdrawal in a single month?


SELECT
    month_no,
    COUNT(*) AS customer_count
FROM
(
    SELECT
        customer_id,
        MONTH(txn_date) AS month_no,
        SUM(CASE WHEN txn_type='deposit' THEN 1 ELSE 0 END) AS deposit_count,
        SUM(CASE WHEN txn_type='purchase' THEN 1 ELSE 0 END) AS purchase_count,
        SUM(CASE WHEN txn_type='withdrawal' THEN 1 ELSE 0 END) AS withdrawal_count
    FROM customer_transactions
    GROUP BY customer_id, MONTH(txn_date)
) t
WHERE deposit_count > 1
AND (purchase_count >= 1 OR withdrawal_count >= 1)
GROUP BY month_no
ORDER BY month_no;


---
-- B. Customer Transactions

-- 1. What is the unique count and total amount for each transaction type?
SELECT 
txn_type,
SUM(txn_amount) as total_amount,
COUNT(*) as transcation_count
FROM customer_transactions
GROUP BY txn_type;


-- 2. What is the average total historical deposit counts and amounts for all customers
WITH CTE AS (
SELECT 
customer_id,
AVG(txn_amount) as avg_deposit,
COUNT(*) as transaction_count
FROM customer_transactions
WHERE txn_type = 'deposit'
GROUP BY customer_id
)
SELECT 
ROUND(AVG(avg_deposit),2) as avg_deposit_amount,
ROUND(AVG(transaction_count),0) as avg_transactions
FROM CTE;

-- 3. For each month - how many Data Bank customers make more than 1 deposit and either 1 purchase or 1 withdrawal in a single month?
WITH CTE AS (
    SELECT 
        FORMAT(txn_date, 'yyyy-MM') AS month,  -- truncates to month
        customer_id,
        SUM(CASE WHEN txn_type = 'deposit' THEN 1 ELSE 0 END) AS deposits,
        SUM(CASE WHEN txn_type <> 'deposit' THEN 1 ELSE 0 END) AS purchase_or_withdrawal
    FROM customer_transactions
    GROUP BY FORMAT(txn_date, 'yyyy-MM'), customer_id
    HAVING SUM(CASE WHEN txn_type = 'deposit' THEN 1 ELSE 0 END) > 1
       AND SUM(CASE WHEN txn_type <> 'deposit' THEN 1 ELSE 0 END) = 1
)
SELECT 
    month,
    COUNT(customer_id) AS customers
FROM CTE
GROUP BY month;
