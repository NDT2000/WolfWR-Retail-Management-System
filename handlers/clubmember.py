from db import connect_to_db

# Select customer details based on customer_id
def select_customer(customer_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM ClubMember
        WHERE CustomerID = %s
    """, (customer_id,))
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print("Merchandise details:")
    for result in results:
        for column, value in zip(columns, result):
            print(f"{column}: {value}")
        print("-" * 20)  # Separator between records
    cursor.close()
    conn.close()

# Update customer details based on customer_id and provided arguments
def update_customer(customer_id, args):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Mapping keys to column names
    key_to_column = {
        "first_name": "FirstName",
        "last_name": "LastName",
        "age": "Age",
        "membership_level": "MembershipLevel",
        "home_address": "HomeAddress",
        "phone": "PhoneNumber",
        "email": "EmailAddress",
        "active": "ActiveStatus"
    }

    # Filter and map keys to columns
    updates = ", ".join([
        f"{key_to_column[key]} = {args[key]}" if not isinstance(args[key], str) else f"{key_to_column[key]} = '{args[key]}'"
        for key in args.keys() if key in key_to_column and args[key] is not None
    ])

    primary_keys = [customer_id]

    cursor.execute(f"""
        UPDATE ClubMember
        SET {updates}
        WHERE CustomerID=%s
    """, (primary_keys))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Customer {customer_id} updated.")

# Set customer status to inactive based on customer_id
def delete_customer(customer_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ClubMember
        SET ActiveStatus = FALSE
        WHERE CustomerID = %s
    """, (customer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Customer {customer_id} set to inactive.")
