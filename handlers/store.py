from db import connect_to_db

# Function to select a store by its ID and display its details
def select_store(store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Store WHERE StoreID=%s", (store_id,))
    store = cursor.fetchone()
    if store:
        columns = [desc[0] for desc in cursor.description]
        print("Staff details:")
        for column, value in zip(columns, store):
            print(f"{column}: {value}")
        print("-" * 20)  # Separator between records
    else:
        print("No store found")
    cursor.close()
    conn.close()

# Function to add a new store
def add_store(store_id, address, phone, manager_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    if manager_id is None:
        cursor.execute("""
            INSERT INTO Store (StoreID, StoreAddress, PhoneNumber, ManagerID)
            VALUES (%s, %s, %s, NULL)
        """, (store_id, address, phone))
    else:
        cursor.execute("""
            INSERT INTO Store (StoreID, StoreAddress, PhoneNumber, ManagerID)
            VALUES (%s, %s, %s, %s)
        """, (store_id, address, phone, manager_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Store {store_id} added.")

# Function to update an existing store's details
def update_store(store_id, address, phone, manager_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        if manager_id is None:
            cursor.execute("""
                UPDATE Store SET StoreAddress=%s, PhoneNumber=%s
                WHERE StoreID=%s
            """, (address, phone, store_id))
        else:
            cursor.execute("""
                UPDATE Store SET StoreAddress=%s, PhoneNumber=%s, ManagerID=%s
                WHERE StoreID=%s
            """, (address, phone, manager_id, store_id))
        conn.commit()
        print(f"Store {store_id} updated.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating store: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to delete a store
def delete_store(store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Store WHERE StoreID=%s", (store_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Store {store_id} deleted.")
