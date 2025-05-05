from db import connect_to_db

# Function to retrieve details of a supplier transaction by its ID
def select_supplier_transaction(transaction_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM SupplierTransaction
        WHERE TransactionID = %s
    """, (transaction_id,))
    transaction = cursor.fetchone()
    if transaction:
        columns = [desc[0] for desc in cursor.description]
        print("Supplier transaction details:")
        for column, value in zip(columns, transaction):
            print(f"{column}: {value}")
        print("-" * 20)  # Separator between records
    else:
        print("No supplier transaction found.")
    cursor.close()
    conn.close()

# Function to add a new supplier transaction to the database
def add_supplier_transaction(transaction_id, supplier_id, store_id, product_id, quantity, purchase_date, cost):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Insert the supplier transaction
        cursor.execute("""
            INSERT INTO SupplierTransaction (TransactionID, SupplierID, StoreID, ProductID, Quantity, PurchaseDate, Cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (transaction_id, supplier_id, store_id, product_id, quantity, purchase_date, cost))
        
        # Update the quantity of the product in Merchandise
        cursor.execute("""
            UPDATE Merchandise
            SET Quantity = Quantity + %s
            WHERE StoreID = %s AND ProductID = %s
        """, (quantity, store_id, product_id))

        conn.commit()
        print(f"Supplier transaction {transaction_id} added.")
    except Exception as e:
        # Rollback in case of an error
        conn.rollback()
        print(f"Error making transaction: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to update an existing supplier transaction in the database
def update_supplier_transaction(transaction_id, supplier_id, store_id, product_id, quantity, purchase_date, cost):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE SupplierTransaction SET SupplierID=%s, StoreID=%s, ProductID=%s, Quantity=%s, PurchaseDate=%s, Cost=%s
        WHERE TransactionID=%s
    """, (supplier_id, store_id, product_id, quantity, purchase_date, cost, transaction_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Supplier transaction {transaction_id} updated.")

# Function to delete a supplier transaction by its ID
def delete_supplier_transaction(transaction_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SupplierTransaction WHERE TransactionID=%s", (transaction_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Supplier transaction {transaction_id} deleted.")
