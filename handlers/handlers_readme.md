# WolfWR Retail Management System

## Handlers Overview

### clubmember.py
- Provides a set of functions to interact with the customer records stored in the **ClubMember** table.
- **select_customer**: Retrieves and displays all details for a given customer by their ID, formatting the results for clarity.
- **update_customer**: Builds and executes a dynamic SQL UPDATE query using a mapping between provided argument keys and database column names; updates only the fields for which new values are provided.
- **delete_customer**: Marks a customer as inactive by setting the ActiveStatus field to FALSE rather than physically removing the record.

---

### customer_transaction.py
- Manages all aspects of customer transactions within the system.
- **select_customer_transaction**: Retrieves transaction metadata and joins with the merchandise table to provide detailed product information along with the computed total cost.
- **add_customer_transaction**: Validates the customer's active membership status based on the purchase date, applies any relevant discounts, computes the total cost, inserts the transaction into the database, and updates the inventory to reflect the sale.
- **update_customer_transaction**: Adjusts the transaction details and corrects the inventory based on any change in purchase quantity.
- **delete_customer_transaction**: Restores the inventory for the products involved before deleting the transaction record.
- **return_customer_items**: Processes returns by adjusting the quantity and cost in the transaction record while incrementing the inventory accordingly.

---

### discount.py
- Manages discount-related operations by interfacing with the **Discount** table in the database.
- **select_discount**: Retrieves and displays the discount details for a specified product at a given store, formatting the output record by record.
- **add_discount**: Inserts a new discount record into the **Discount** table using details such as discount percentage, start date, and end date.
- **delete_discount**: Removes an existing discount record based on the provided product and store IDs.

---

### merchandise.py
- Provides a comprehensive set of functions for managing merchandise records.
- **select_merchandise**: Retrieves merchandise details based on product and/or store identifiers.
- **create_merchandise**: Adds new merchandise entries into the database.
- **update_merchandise**: Updates existing merchandise records by dynamically constructing SQL update statements from provided arguments.
- **delete_merchandise**: Deletes merchandise records from the system.
- **transfer_merchandise**: Supports transferring inventory between stores by decreasing the quantity in the original store and either adding or updating the record in the destination store.

---

### signup.py
- Handles operations related to membership sign-ups and membership level updates.
- **select_signup**: Retrieves and displays details of a specific signup entry based on the signup ID.
- **add_signup**: Inserts a new customer into the **ClubMember** table and simultaneously logs their sign-up in the **SignUp** table.
- **update_membership_via_signup**: Updates a customer's membership level in the **ClubMember** table and records the change by adding a new row in the **SignUp** table.

---

### staff.py
- Responsible for managing staff data.
- **select_staff_by_parameter**: Retrieves staff details based on either a provided staff ID or store ID by dynamically constructing the query condition.
- **add_staff**: Inserts a new staff record into the database with details such as names, age, address, job title, employment time, phone number, email, and store identifier.
- **update_staff**: Dynamically updates specific fields of an existing staff record by mapping provided keys to database column names.
- **delete_staff**: Removes a staff record identified by a given staff ID.

---

### store.py
- Manages store records in the database.
- **select_store**: Retrieves and displays store details based on a specified store ID.
- **add_store**: Adds a new store to the database by inserting details like the store address, phone number, and manager ID.
- **update_store**: Updates an existing store’s information by replacing the store address, phone number, and manager ID with new values.
- **delete_store**: Deletes a store record from the database based on its store ID.

---

### supplier.py
- Manages supplier records.
- **select_supplier**: Retrieves a supplier’s details from the database based on the provided supplier ID, printing each column and its corresponding value in a user-friendly format.
- **add_supplier**: Inserts a new supplier into the **Supplier** table with key information such as supplier name, home address, phone number, email, and the associated staff ID.
- **update_supplier**: Updates an existing supplier’s information with new data.
- **delete_supplier**: Removes a supplier record from the system based on the given supplier ID.

---

### supplier_transaction.py
- Dedicated to managing supplier transactions.
- **select_supplier_transaction**: Retrieves and displays all details associated with a specific transaction ID from the **SupplierTransaction** table.
- **add_supplier_transaction**: Handles the insertion of a new supplier transaction; it records the transaction details and updates the corresponding merchandise inventory by increasing the product's quantity.
- **update_supplier_transaction**: Updates an existing supplier transaction with new details, ensuring corrections are committed to the database.
- **delete_supplier_transaction**: Deletes a supplier transaction record based on the provided transaction ID.

---

