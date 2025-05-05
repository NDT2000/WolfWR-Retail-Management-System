from db import connect_to_db

# Function to select a supplier by their ID and display their details
def select_supplier(supplier_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Supplier WHERE SupplierID=%s", (supplier_id,))
    supplier = cursor.fetchone()
    if supplier:
        columns = [desc[0] for desc in cursor.description]
        print("Supplier details:")
        for column, value in zip(columns, supplier):
            print(f"{column}: {value}")
        print("-" * 20)  # Separator between records
    else:
        print("No supplier found")
    cursor.close()
    conn.close()

# Function to add a new supplier
def add_supplier(supplier_id, supplier_name, home_address, phone, email, staff_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Supplier (SupplierID, SupplierName, HomeAddress, PhoneNumber, EmailAddress, StaffID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (supplier_id, supplier_name, home_address, phone, email, staff_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Supplier {supplier_id} added.")

# Function to update an existing supplier's details
def update_supplier(supplier_id, args):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Mapping keys to column names
    key_to_column = {
        "supplier_name": "SupplierName",
        "home_address": "HomeAddress",
        "phone": "PhoneNumber",
        "email": "EmailAddress",
        "staff_id": "StaffID",
    }

    # Filter and map keys to columns
    updates = ", ".join([
        f"{key_to_column[key]} = {args[key]}" if not isinstance(args[key], str) else f"{key_to_column[key]} = '{args[key]}'"
        for key in args.keys() if key in key_to_column and args[key] is not None
    ])

    primary_keys = [supplier_id]

    cursor.execute(f"""
        UPDATE Supplier SET {updates}
        WHERE SupplierID=%s
    """, (primary_keys))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Supplier {supplier_id} updated.")

# Function to delete a supplier
def delete_supplier(supplier_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Supplier WHERE SupplierID=%s", (supplier_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Supplier {supplier_id} deleted.")