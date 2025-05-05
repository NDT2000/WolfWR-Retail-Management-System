from db import connect_to_db
from datetime import datetime

# Fetch customer transaction details based on transaction_id
def select_customer_transaction(transaction_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    # Fetch all transaction details for the given transaction ID
    cursor.execute("""
        SELECT CustomerID, StaffID, StoreID, PurchaseDate
        FROM CustomerTransaction
        WHERE TransactionNumber = %s
    """, (transaction_id,))
    common_details = cursor.fetchone()
    if not common_details:
        print("Transaction not found.")
        return None
    customer_id, staff_id, store_id, purchase_date = common_details

    # Fetch product details for the given transaction
    cursor.execute("""
        SELECT Merchandise.ProductID, Merchandise.Productname, CustomerTransaction.Quantity, TotalCost
        FROM CustomerTransaction JOIN Merchandise ON CustomerTransaction.ProductID = Merchandise.ProductID
        WHERE TransactionNumber = %s
    """, (transaction_id,))
    product_details = cursor.fetchall()


    cursor.execute("""
        SELECT SUM(TotalCost)
        FROM CustomerTransaction
        WHERE TransactionNumber = %s
    """, (transaction_id,))
    total_cost = float(cursor.fetchone()[0])

    # Display transaction and product details
    print(f"Transaction details for {transaction_id}:")
    print(f"CustomerID: {customer_id}, StaffID: {staff_id}, StoreID: {store_id}, PurchaseDate: {purchase_date}")
    for product in product_details:
        print(f"ProductID: {product[0]}, Product Name: {product[1]}, Quantity: {product[2]}, Cost: {product[3]}")
    print(f"Total cost of transaction {transaction_id}: {total_cost}")

# Add a new customer transaction, update inventory, and check active status
def add_customer_transaction(transaction_id, product_id, store_id, customer_id, staff_id, quantity, purchase_date):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        if purchase_date == "current":
            # Check if member's current active status is True
            cursor.execute("""
                SELECT ActiveStatus FROM ClubMember
                WHERE CustomerID = %s
            """, (customer_id,))
            active_status = cursor.fetchone()
            if not active_status or not active_status[0]:
                raise ValueError("Customer is not an active member.")
            purchase_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # Check if customer was active member during the purchase date
            purchase_date_obj = datetime.strptime(purchase_date, "%Y-%m-%d")
            purchase_date_minus_year = purchase_date_obj.replace(year=purchase_date_obj.year - 1)
            cursor.execute("""
                SELECT * FROM SignUp
                WHERE CustomerID = %s AND SignUpDate BETWEEN %s AND %s
            """, (customer_id, purchase_date_minus_year.strftime("%Y-%m-%d"), purchase_date))
            if not cursor.fetchone():
                raise ValueError("Customer was not an active member during the purchase date.")

        # Fetch market price for the product
        cursor.execute("""
            SELECT MarketPrice FROM Merchandise
            WHERE ProductID = %s AND StoreID = %s
        """, (product_id, store_id))
        result = cursor.fetchone()
        if not result:
            raise ValueError("Product not found in the specified store.")
        market_price = float(result[0])

        # Calculate total cost
        # Check if a discount applies to the product
        cursor.execute("""
            SELECT DiscountPercentage FROM Discount
            WHERE ProductID = %s AND StoreID = %s AND %s BETWEEN StartDate AND EndDate
        """, (product_id, store_id, purchase_date))
        discount_result = cursor.fetchone()
        discount_percentage = float(discount_result[0]) if discount_result else 0

        # Calculate total cost with discount
        total_cost = market_price * quantity * (1 - discount_percentage / 100)
        cursor.execute("""
            INSERT INTO CustomerTransaction (TransactionNumber, ProductID, StoreID, CustomerID, StaffID, Quantity, PurchaseDate, TotalCost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (transaction_id, product_id, store_id, customer_id, staff_id, quantity, purchase_date, total_cost))

        # Reduce inventory
        cursor.execute("""
            UPDATE Merchandise
            SET Quantity = Quantity - %s
            WHERE ProductID = %s AND StoreID = %s
        """, (quantity, product_id, store_id))

        conn.commit()
        print(f"Customer transaction {transaction_id} added and inventory updated.")
    except Exception as e:
        conn.rollback()
        print(f"Error adding transaction: {e}")
    finally:
        cursor.close()
        conn.close()

# Update an existing customer transaction and adjust inventory accordingly
def update_customer_transaction(transaction_id, product_id, store_id, customer_id, staff_id, quantity, purchase_date, total_cost):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Get previous quantity to adjust stock
        cursor.execute("""
            SELECT Quantity FROM CustomerTransaction WHERE TransactionName = %s
        """, (transaction_id,))
        previous_quantity = cursor.fetchone()[0]

        # Update transaction
        cursor.execute("""
            UPDATE CustomerTransaction
            SET ProductID=%s, StoreID=%s, CustomerID=%s, StaffID=%s,
                Quantity=%s, PurchaseDate=%s, TotalCost=%s
            WHERE TransactionID=%s
        """, (product_id, store_id, customer_id, staff_id, quantity, purchase_date, total_cost, transaction_id))

        # Adjust inventory
        quantity_difference = previous_quantity - quantity
        cursor.execute("""
            UPDATE Merchandise
            SET Quantity = Quantity + %s
            WHERE ProductID = %s AND StoreID = %s
        """, (quantity_difference, product_id, store_id))

        conn.commit()
        print(f"Customer transaction {transaction_id} updated and inventory adjusted.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating transaction: {e}")
    finally:
        cursor.close()
        conn.close()

# Delete a customer transaction and restore inventory to its original state
def delete_customer_transaction(transaction_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Get product info before deletion
        cursor.execute("""
            SELECT ProductID, StoreID, Quantity FROM CustomerTransaction
            WHERE TransactionNumber = %s
        """, (transaction_id,))
        results = cursor.fetchall()
        for result in results:
            if not result:
                print("Transaction not found.")
                return
            product_id, store_id, quantity = result

            # Restore inventory
            cursor.execute("""
                UPDATE Merchandise
                SET Quantity = Quantity + %s
                WHERE ProductID = %s AND StoreID = %s
            """, (quantity, product_id, store_id))

        # Delete transaction
        cursor.execute("""
            DELETE FROM CustomerTransaction
            WHERE TransactionNumber = %s
        """, (transaction_id,))

        conn.commit()
        print(f" Transaction {transaction_id} deleted and inventory restored.")
    except Exception as e:
        conn.rollback()
        print(f" Error deleting transaction: {e}")
    finally:
        cursor.close()
        conn.close()

# Process item returns from a transaction and update inventory
def return_customer_items(transaction_id, product_id, store_id, return_quantity):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Get the transaction
        cursor.execute("""
            SELECT ProductID, StoreID, Quantity, TotalCost FROM CustomerTransaction
            WHERE TransactionNumber = %s
                AND ProductID = %s
                AND StoreID = %s
        """, (transaction_id, product_id, store_id))
        result = cursor.fetchone()
        if not result:
            print("Transaction not found.")
            return
        product_id, store_id, bought_quantity, total_cost = result

        if bought_quantity < return_quantity:
            raise ValueError("Return quantity exceeds purchased quantity.")

        # Restore inventory
        cursor.execute("""
            UPDATE Merchandise
            SET Quantity = Quantity + %s
            WHERE ProductID = %s AND StoreID = %s
        """, (return_quantity, product_id, store_id))

        # Update transaction with new quantity and cost
        per_item_cost = total_cost / bought_quantity
        new_total_cost = per_item_cost * (bought_quantity - return_quantity)
        cursor.execute("""
            UPDATE CustomerTransaction
            SET Quantity = Quantity - %s,
                TotalCost = %s
            WHERE TransactionNumber = %s AND ProductID = %s AND StoreID = %s
        """, (return_quantity, new_total_cost, transaction_id, product_id, store_id))

        conn.commit()
        print(f"Returned {return_quantity} item(s) for transaction {transaction_id}. Inventory updated.")
    except Exception as e:
        conn.rollback()
        print(f"Error processing return: {e}")
    finally:
        cursor.close()
        conn.close()
