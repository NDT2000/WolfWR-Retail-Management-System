"""
Module: sales.py
Description: Provides reporting functionality for WolfWR.
This module contains:
  - get_sales_report(by, store_id=None): Generates a sales report grouped by day, month, or year.
  - get_sales_growth_report(store_id, start_date, end_date): Generates a sales growth report for a store over a period.
Usage:
  To generate a sales report:
    python3 sales.py sales --by <day|month|year> [--store_id <store_id>]
  To generate a sales growth report:
    python3 sales.py growth --store_id <store_id> --start_date YYYY-MM-DD --end_date YYYY-MM-DD
Note: Adjust SQL date formatting functions if using a DBMS other than MySQL.
"""

from db import connect_to_db  # Make sure your db.py provides a working connect_to_db()

def get_sales_report(by, store_id=None):
    """
    Generate a sales report grouped by the specified time unit.
    
    Parameters:
      by (str): One of "day", "month", or "year" for grouping.
      store_id (str, optional): If provided, filters by store.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        if by == "day":
            group_clause = "DATE(PurchaseDate)"
            select_clause = "DATE(PurchaseDate) as period"
        elif by == "month":
            group_clause = "DATE_FORMAT(PurchaseDate, '%Y-%m')"
            select_clause = "DATE_FORMAT(PurchaseDate, '%Y-%m') as period"
        elif by == "year":
            group_clause = "YEAR(PurchaseDate)"
            select_clause = "YEAR(PurchaseDate) as period"
        else:
            print("Invalid grouping provided. Choose from 'day', 'month', or 'year'.")
            return

        query = f"""
            SELECT {select_clause}, SUM(TotalCost) as total_sales
            FROM CustomerTransaction
        """
        params = []
        if store_id:
            query += " WHERE StoreID = %s"
            params.append(store_id)
        query += f" GROUP BY {group_clause} ORDER BY {group_clause}"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            print("No sales data found.")
        else:
            print(f"\nSales Report grouped by {by}:")
            print("-" * 40)
            for row in rows:
                print(f"Period: {row[0]}, Total Sales: {row[1]}")
            print("-" * 40)
    except Exception as e:
        print("Error generating sales report:", e)
    finally:
        cursor.close()
        conn.close()

def get_sales_growth_report(store_id, start_date, end_date):
    """
    Generate a sales growth report for a specific store and period.
    
    Parameters:
      store_id (str): The store to report on.
      start_date (str): Report start date (YYYY-MM-DD).
      end_date (str): Report end date (YYYY-MM-DD).
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        query = """
            SELECT DATE_FORMAT(PurchaseDate, '%Y-%m') as period, SUM(TotalCost) as total_sales
            FROM CustomerTransaction
            WHERE StoreID = %s AND PurchaseDate BETWEEN %s AND %s
            GROUP BY period
            ORDER BY period
        """
        cursor.execute(query, (store_id, start_date, end_date))
        rows = cursor.fetchall()
        if not rows:
            print("No sales data found for the specified period.")
            return

        print(f"\nSales Growth Report for Store {store_id} from {start_date} to {end_date}")
        print("-" * 60)
        previous_sales = None
        for row in rows:
            period, total_sales = row
            print(f"Period: {period}, Sales: {total_sales}", end='')
            if previous_sales is not None:
                if previous_sales != 0:
                    growth = ((total_sales - previous_sales) / previous_sales) * 100
                else:
                    growth = float('inf')
                print(f", Growth: {growth:.2f}%")
            else:
                print(" (first period)")
            previous_sales = total_sales

        first_sales = rows[0][1]
        last_sales = rows[-1][1]
        overall_growth = ((last_sales - first_sales) / first_sales * 100) if first_sales != 0 else float('inf')
        print("-" * 60)
        print(f"Overall growth from {rows[0][0]} to {rows[-1][0]}: {overall_growth:.2f}%")
        print("-" * 60)
    except Exception as e:
        print("Error generating sales growth report:", e)
    finally:
        cursor.close()
        conn.close()

# Allow direct module testing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sales Reporting for WolfWR")
    subparsers = parser.add_subparsers(dest="action", help="Choose 'sales' or 'growth' report")

    # Sales report subcommand
    sales_parser = subparsers.add_parser("sales", help="Generate sales report")
    sales_parser.add_argument("--by", choices=["day", "month", "year"], required=True, help="Grouping unit")
    sales_parser.add_argument("--store_id", help="Store ID for filtering (optional)")

    # Sales growth report subcommand
    growth_parser = subparsers.add_parser("growth", help="Generate sales growth report")
    growth_parser.add_argument("--store_id", required=True, help="Store ID for the report")
    growth_parser.add_argument("--start_date", required=True, help="Start date (YYYY-MM-DD)")
    growth_parser.add_argument("--end_date", required=True, help="End date (YYYY-MM-DD)")

    args = parser.parse_args()
    if args.action == "sales":
        get_sales_report(args.by, args.store_id)
    elif args.action == "growth":
        get_sales_growth_report(args.store_id, args.start_date, args.end_date)
    else:
        parser.print_help()
