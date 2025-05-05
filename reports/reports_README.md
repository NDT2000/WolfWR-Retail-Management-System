# WolfWR Retail Management System

## Reports Overview

This document provides an overview of the reporting modules for the WolfWR Retail Management System. Each section below describes a specific report file, its purpose, and a summary of its functionality.

---

## customer_activity.py

This code file generates a customer activity report for a specified customer over a given date range. The **get_customer_activity_report** function connects to the database using a shared connection helper and then executes a SQL query that joins the CustomerTransaction and ClubMember tables to retrieve the customer's first and last name, count distinct transactions, and calculate the total amount spent. It formats and prints out these details, providing a clear summary of the customer's transaction history within the specified dates, while also incorporating error handling with commit and rollback mechanisms and ensuring proper cleanup by closing the cursor at the end.

---

## customer_growth.py

This code file generates a report on customer growth over time based on sign-up data. The **get_customer_growth_report** function establishes a connection to the database, then checks whether the report should be aggregated by month or by year. Depending on the parameter provided, it constructs and executes a SQL query that groups sign-up records by the formatted sign-up date (either as a month or as a year) and counts the total number of sign-ups for each period. The results are displayed in a formatted table showing the period and the corresponding count of new customers. Additionally, the function includes robust error handling with rollback procedures and ensures that both the cursor and the connection are properly closed after execution.

---

## reward_check.py

This code connects to the database to retrieve a customer’s membership history and identifies the time intervals during which the customer held a Platinum membership. For each Platinum period, it calculates a cashback reward of 2% based on the total spending recorded in customer transactions during that interval. Finally, these rewards are summed to determine the customer’s total cashback, which is then printed out, ensuring that the entire process is executed with proper error handling and database resource management.

---

## sales.py

This module provides comprehensive sales reporting functionality for the WolfWR Retail Management System. It includes two main functions: **get_sales_report**, which dynamically groups and sums total sales by day, month, or year (with optional store filtering), and **get_sales_growth_report**, which calculates and displays the growth of sales over a specified period for a given store. Both functions use a secure database connection via **connect_to_db**, execute robust SQL queries with error handling and rollback mechanisms as needed, and ensure proper resource cleanup by closing cursors and connections after use. The module also incorporates a command-line interface using argparse, enabling users to easily generate and view sales and growth reports directly from the terminal.

---

## stock.py

This code defines the **get_stock_report** function, which retrieves inventory data from the Merchandise table based on the provided parameters. It executes different SQL queries depending on whether a store ID or product ID is supplied (or both). For instance, if only a store ID is provided, it fetches all merchandise records for that store; if only a product ID is given, it first retrieves the total quantity of that product and then its detailed records; if both are provided, it retrieves the specific record matching the product and store combination. The results are formatted and printed, and the function ensures proper cleanup by closing both the cursor and the database connection.

---

## supplier_bill.py

This code file defines the **generate_supplier_bill** function, which calculates and prints the total cost of supplier transactions for a given supplier and year. It connects to the database, executes a SQL query that sums the Cost from the SupplierTransaction table for the specified supplier and year, and then prints the resulting total cost formatted as a dollar amount. If no transactions are found, it outputs an appropriate message. Finally, the function ensures proper cleanup by closing both the cursor and the database connection.

---