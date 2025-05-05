from db import connect_to_db

def get_customer_activity_report(customer_id, start_date, end_date):
    # Establish a connection and create a cursor
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # SQL query to fetch customer activity details
        query = """
            SELECT FirstName, LastName, COUNT(DISTINCT TransactionID), SUM(TotalCost) AS TotalSpent
            FROM CustomerTransaction JOIN ClubMember ON CustomerTransaction.CustomerID = ClubMember.CustomerID
            WHERE CustomerTransaction.CustomerID = ?
            AND PurchaseDate BETWEEN ? AND ?
            GROUP BY CustomerTransaction.CustomerID, ClubMember.FirstName, ClubMember.LastName;
        """
        # Execute query with parameters
        cursor.execute(query, (customer_id, start_date, end_date))
        result = cursor.fetchone()
        
        # Check if a result was returned and print report details
        if result:
            first_name, last_name, transaction_count, total_spent = result
            print(f"Customer {customer_id} ({first_name} {last_name}) made {transaction_count} transactions from {start_date} to {end_date}")
            print(f"Total spent: ${total_spent:.2f}")
        else:
            print(f"No transactions found for customer {customer_id} from {start_date} to {end_date}.")
        
        # Commit the transaction after successful query execution
        conn.commit()
    except Exception as e:
        # Rollback if any error occurs
        print(f"Database error during report generation: {e}")
        conn.rollback()
    finally:
        # Ensure the cursor is properly closed
        cursor.close()