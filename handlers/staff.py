from db import connect_to_db

# Function to select and display staff details by staff_id or store_id
def select_staff_by_parameter(staff_id, store_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    if staff_id is not None:
        column = "StaffID"
        value = staff_id
    elif store_id is not None:
        column = "StoreID"
        value = store_id
    else:
        raise ValueError("Both 'staff_id' and 'store_id' cannot be None.")

    query = f"SELECT * FROM Staff WHERE {column} = %s"
    cursor.execute(query, (value,))
    results = cursor.fetchall()
    if results:
        columns = [desc[0] for desc in cursor.description]
        print("Staff details:")
        for result in results:
            for column, value in zip(columns, result):
                print(f"{column}: {value}")
            print("-" * 20)  # Separator between records
    else:
        print("No staff found.")
    cursor.close()
    conn.close()

# Function to add a new staff member to the database
def add_staff(staff_id, first_name, last_name, age, home_address, job_title, employment_time, phone, email, store_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Staff (StaffID, FirstName, LastName, Age, HomeAddress, JobTitle,
                           TimeOfEmployment, PhoneNumber, EmailAddress, StoreID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (staff_id, first_name, last_name, age, home_address, job_title,
          employment_time, phone, email, store_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Staff {staff_id} added.")

# Function to update existing staff member details
def update_staff(staff_id, args):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Mapping keys to column names
    key_to_column = {
        "first_name": "FirstName",
        "last_name": "LastName",
        "age": "Age",
        "job_title": "JobTitle",
        "employment_time": "TimeOfEmployment",
        "home_address": "HomeAddress",
        "phone": "PhoneNumber",
        "email": "EmailAddress",
        "store_id": "StoreID"
    }

    # Filter and map keys to columns
    updates = ", ".join([
        f"{key_to_column[key]} = {args[key]}" if not isinstance(args[key], str) else f"{key_to_column[key]} = '{args[key]}'"
        for key in args.keys() if key in key_to_column and args[key] is not None
    ])

    primary_keys = [staff_id]

    cursor.execute(f"""
        UPDATE Staff
        SET {updates}
        WHERE StaffID=%s
    """, (primary_keys))
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Staff {staff_id} updated.")

# Function to delete a staff member from the database
def delete_staff(staff_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Staff WHERE StaffID = %s", (staff_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Staff {staff_id} deleted.")
