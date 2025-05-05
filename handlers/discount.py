from db import connect_to_db

# Function to retrieve and print discount details based on product and store
def select_discount(product_id, store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Discount WHERE ProductID = %s AND StoreID = %s", (product_id, store_id))
    discounts = cursor.fetchall()
    if discounts:
        columns = [desc[0] for desc in cursor.description]
        for discount in discounts:
            print("Discount details:")
            for column, value in zip(columns, discount):
                print(f"{column}: {value}")
            print("-" * 20)  # Separator between records
    else:
        print("No discount found.")
    cursor.close()
    conn.close()

# Function to add a new discount for a product at a store
def add_discount(product_id, store_id, percentage, start_date, end_date):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Discount (ProductID, StoreID, DiscountPercentage, StartDate, EndDate)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_id, store_id, percentage, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Discount added for Product {product_id} at Store {store_id}.")

# Function to delete a discount for a product at a store
def delete_discount(product_id, store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Discount WHERE ProductID = %s AND StoreID = %s ", (product_id, store_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Discount removed for Product {product_id} at Store {store_id}.")
