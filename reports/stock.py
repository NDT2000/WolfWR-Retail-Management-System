from db import connect_to_db

def get_stock_report(product_id, store_id):
    # Establish connection and create a cursor
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Execute appropriate query based on provided parameters
    if product_id is None and store_id is not None:
        # Retrieve all merchandise records for the given store
        cursor.execute("""
            SELECT * FROM Merchandise
            WHERE StoreID = %s
        """, (store_id,))
    elif store_id is None and product_id is not None:
        # Calculate total quantity for the specific product
        cursor.execute("""
            SELECT SUM(Quantity) FROM Merchandise
            WHERE ProductID = %s
        """, (product_id,))
        total_quantity = cursor.fetchone()[0]
        print("Total Quantity: ", total_quantity)

        # Retrieve detailed records for the product
        cursor.execute("""
            SELECT * FROM Merchandise
            WHERE ProductID = %s
        """, (product_id,))
    else:
        # Retrieve records matching both product and store identifiers
        cursor.execute("""
            SELECT * FROM Merchandise
            WHERE ProductID = %s AND StoreID = %s
        """, (product_id, store_id))
    
    # Fetch and display results in a formatted manner
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
        
    # Clean up resources
    cursor.close()
    conn.close()