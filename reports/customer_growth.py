from db import connect_to_db

def get_customer_growth_report(by, value=None):
    # Establish database connection and create a cursor
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Choose SQL query based on grouping option: month or year
        if by == "month":
            query = """
                SELECT DATE_FORMAT(SignUpDate, '%Y-%m') AS Period, COUNT(DISTINCT CustomerID) AS CustomerID
                FROM SignUp
                GROUP BY Period
                ORDER BY Period;
            """
        elif by == "year":
            query = """
                SELECT YEAR(SignUpDate) AS Period, COUNT(DISTINCT CustomerID) AS CustomerID
                FROM SignUp
                GROUP BY Period
                ORDER BY Period;
            """
        else:
            print("Invalid option. Please choose 'month' or 'year'.")
            return
        
        # Execute the query and fetch results
        cursor.execute(query)
        results = cursor.fetchall()
        
        
        # Print the report header and details in a formatted manner
        
        print(f"{'Period':<10} | {'New Customers':<15}")
        print("-" * 30)
        for row in results:
            print(f"{row[0]:<10} | {row[1]:<15}")

    except Exception as e:
        # Print error details and rollback transaction in case of failure
        print(f"Error fetching customer growth: {e}")
        conn.rollback()
    finally:
        # Clean up by closing cursor and connection
        cursor.close()
        conn.close()
