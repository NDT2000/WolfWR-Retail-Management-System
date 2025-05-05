from db import connect_to_db

# Function to retrieve and print merchandise details based on product and store
def select_merchandise(product_id, store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    if product_id is None and store_id is not None:
        cursor.execute("""
            SELECT * FROM Merchandise
            WHERE StoreID = %s
        """, (store_id,))
    elif store_id is None and product_id is not None:
        cursor.execute("""
            SELECT * FROM Merchandise
            WHERE ProductID = %s
        """, (product_id,))
    elif store_id is not None and product_id is not None:
        cursor.execute("""
            SELECT * FROM Merchandise
            WHERE ProductID = %s AND StoreID = %s
        """, (product_id, store_id))
    results = cursor.fetchall()
    if results:
        columns = [desc[0] for desc in cursor.description]
        print("Merchandise details:")
        for result in results:
            for column, value in zip(columns, result):
                print(f"{column}: {value}")
            print("-" * 20)  # Separator between records
    else:
        print("No merchandise found.")
    cursor.close()
    conn.close()

# Function to create new merchandise entry
def create_merchandise(product_id, store_id, product_name, quantity, buy_price, market_price, production_date, expiration_date, supplier_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Merchandise (ProductID, StoreID, ProductName, Quantity, BuyPrice, MarketPrice, ProductionDate, ExpirationDate, SupplierID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (product_id, store_id, product_name, quantity, buy_price, market_price, production_date, expiration_date, supplier_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Merchandise {product_id} {store_id} added.")

# Function to update existing merchandise details
def update_merchandise(product_id, store_id, args):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Mapping keys to column names
    key_to_column = {
        "product_name": "ProductName",
        "quantity": "Quantity",
        "buy_price": "BuyPrice",
        "market_price": "MarketPrice",
        "production_date": "ProductionDate",
        "expiration_date": "ExpirationDate",
        "supplier_id": "SupplierID"
    }

    # Filter and map keys to columns
    updates = ", ".join([
        f"{key_to_column[key]} = {args[key]}" if not isinstance(args[key], str) else f"{key_to_column[key]} = '{args[key]}'"
        for key in args.keys() if key in key_to_column and args[key] is not None
    ])

    # Add ProductID and StoreID to the values list
    primary_keys = [product_id, store_id]

    cursor.execute(f"""
        UPDATE Merchandise
        SET {updates}
        WHERE ProductID = %s AND StoreID = %s
    """, primary_keys)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Merchandise {product_id} {store_id} updated.")

# Function to delete a merchandise entry
def delete_merchandise(product_id, store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Merchandise
        WHERE ProductID = %s AND StoreID = %s
    """, (product_id, store_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Merchandise {product_id} {store_id} deleted.")

# Function to transfer merchandise between stores
def transfer_merchandise(product_id, original_store_id, new_store_id, quantity):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Decrease inventory in the original store
        cursor.execute("""
            UPDATE Merchandise
            SET Quantity = Quantity - %d
            WHERE ProductID = %s AND StoreID = %s
        """, (quantity, product_id, original_store_id))

        # Check if merchandise exists in the destination store
        cursor.execute("""
            SELECT Quantity FROM Merchandise
            WHERE ProductID = %s AND StoreID = %s
        """, (product_id, new_store_id))
        result = cursor.fetchone()

        if not result:
            # Merchandise does not exist, create it with the transferred quantity and copy other columns
            cursor.execute("""
            INSERT INTO Merchandise (ProductID, StoreID, ProductName, Quantity, BuyPrice, MarketPrice, ProductionDate, ExpirationDate, SupplierID)
            SELECT ProductID, %s, ProductName, %s, BuyPrice, MarketPrice, ProductionDate, ExpirationDate, SupplierID
            FROM Merchandise
            WHERE ProductID = %s AND StoreID = %s
            """, (new_store_id, 0, product_id, original_store_id))
        # Merchandise exists, increase the quantity
        cursor.execute("""
        UPDATE Merchandise
        SET Quantity = Quantity + %s
        WHERE ProductID = %s AND StoreID = %s
        """, (quantity, product_id, new_store_id))

        # Commit the transaction
        conn.commit()
        print(f"Merchandise {product_id} transferred from store {original_store_id} to store {new_store_id}.")
    except Exception as e:
        # Rollback in case of an error
        conn.rollback()
        print(f"Error transferring merchandise: {e}")
    finally:
        cursor.close()
        conn.close()