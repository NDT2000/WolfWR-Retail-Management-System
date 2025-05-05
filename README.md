# WolfWR Retail Management System

A command-line interface (CLI) based retail management system for **WolfWR**, a membership-based wholesale store chain inspired by Costco and Sam’s Club. The system supports full operations for staff, inventory, customer management, supplier coordination, and reporting, backed by a MariaDB database.

## Usage
> usage: cli.py [-h] [--user_type {admin,warehouse_operator,registration_staff,billing_staff,manager}]  
              {store,staff,supplier,member,merchandise,discount,customer_transaction,supplier_transaction,signup,report} ...

> Retail Management System CLI

> positional arguments:  
  Operation group
  {store,staff,supplier,member,merchandise,discount,customer_transaction,supplier_transaction,signup,report}  

> options:  
  -h, --help            show this help message and exit  
  --user_type {admin,warehouse_operator,registration_staff,billing_staff,manager}  
---

## Requirements

### 📖 Narrative
**WolfWR** is a wholesale store chain operating membership-only warehouse clubs. The backend system is used by registration officers, warehouse operators, and billing staff to manage daily operations and reporting.

The system is used to:
- Register and manage staff, suppliers, stores, and customers.
- Record and update merchandise inventory.
- Handle supplier and customer transactions.
- Process returns and apply product discounts.
- Generate various performance and activity reports.
- generate Cashbacks for valued customers

---

## Tasks and Operations

### 1. 🗃️ Information Processing
- Add, update, and delete details for:
  - Stores
  - Staff
  - Suppliers
  - Club members
- Manage product discount details.

### 2. 📦 Maintaining Inventory Records
- Create and update inventory when new merchandise arrives at a store.
- Handle customer returns and reflect the changes in inventory.
- Transfer products between stores.

### 3. 💰 Billing and Transactions
- Record and track supplier transactions during merchandise shipments.
- Process customer purchases and returns.
- Apply automatic price adjustments based on discount rules.
- Compute total price and generate purchase history.
- Track membership rewards for platinum users.

### 4. 📊 Reports
- Total sales report: by day, month, or year.
- Sales growth report for a specific store over a date range.
- Merchandise stock report per product or store.
- Customer growth report (monthly/yearly).
- Customer activity report over a date range.

---

## 📑 Supported Entities and Attributes

| Entity          | Attributes                                                                 |
|-----------------|------------------------------------------------------------------------------|
| **Store**        | Store ID, Manager ID, Store address, Phone number                           |
| **Staff**        | Staff ID, Store ID, Name, Age, Home address, Job title, Phone, Email, Employment time |
| **Supplier**     | Supplier ID, Supplier name, Address, Phone, Email, Staff ID                 |
| **Club Member**  | Customer ID, Name, Membership level (Silver, Gold, Platinum), Address, Phone, Email, Active status |
| **Merchandise**  | Product ID, Product name, Quantity, Buy price, Market price, Dates, Supplier ID, Store ID |
| **Transaction**  | Transaction ID, Product ID, Store ID, Customer ID, Staff ID, Quantity, Date, Cost |
| **Discount**     | Product ID, Store ID, Percentage, Start Date, End Date                      |
| **SignUp**       | Signup ID, Customer ID, Staff ID, Store ID, Membership level, Date          |

---

## ⚙️ Design Assumptions

### Roles & Responsibility
- Registration operators can register/delete staff and suppliers.
- Billing staff handle all transactions, billing, and reward checks.
- Store managers set product prices and discounts.

### Merchandise & Stores
- Merchandise is tracked per store (same product in different stores = separate records).
- All products are available for sale; nothing is held in reserve.
- Shutting down a store deletes all related staff and merchandise.
- Market prices are uniform for the same product across stores.

### Transactions & Returns
- Returns increase merchandise quantity in inventory.
- Returns are recorded using negative quantity transactions.
- Supplier prices are fixed; discounts are only offered by WolfWR.

### Membership & Rewards
- Only **active** members can make purchases.
- **Platinum** members receive **2% cashback** at year-end.
- Membership lasts **1 year** from signup.
- Renewals are recorded as new `signup` entries.

### Data Management
- Date of birth is **not required**.
- Fired staff are **permanently deleted**.
- Supplier stock is considered **unlimited**.
- No charge for **inter-store merchandise transfers**.


