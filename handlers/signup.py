from db import connect_to_db

# Function to select and display signup details by signup_id
def select_signup(signup_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SignUp WHERE SignUpID=%s", (signup_id,))
    signup = cursor.fetchone()
    if signup:
        columns = [desc[0] for desc in cursor.description]
        print("SignUp details:")
        for column, value in zip(columns, signup):
            print(f"{column}: {value}")
        print("-" * 20)  # Separator between records
    else:
        print("No SignUp found.")
    cursor.close()
    conn.close()

# Function to add a new signup and club member into the database
def add_signup(signup_id, staff_id, customer_id, signup_date, store_id, membership_level,
               first_name, last_name, age, home_address, phone, email, active_status):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # 1. Insert into ClubMember
        cursor.execute("""
            INSERT INTO ClubMember (
                CustomerID, FirstName, LastName, Age, MembershipLevel,
                HomeAddress, PhoneNumber, EmailAddress, ActiveStatus
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            customer_id, first_name, last_name, age, membership_level,
            home_address, phone, email, active_status
        ))

        # 2. Insert into SignUp
        cursor.execute("""
            INSERT INTO SignUp (
                SignUpID, StaffID, CustomerID, SignUpDate, StoreID, MembershipLevel
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            signup_id, staff_id, customer_id, signup_date, store_id, membership_level
        ))

        conn.commit()
        print(f"SignUp {signup_id} and ClubMember {customer_id} added.")

    except Exception as e:
        conn.rollback()
        print(f"Error adding SignUp and ClubMember: {e}")

    finally:
        cursor.close()
        conn.close()

# Function to update membership level through signup record
def update_membership_via_signup(signup_id, staff_id, customer_id, signup_date, store_id, new_membership_level):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # 1. Update ClubMember's membership level
        cursor.execute("""
            UPDATE ClubMember
            SET MembershipLevel = %s
            WHERE CustomerID = %s
        """, (new_membership_level, customer_id))

        # 2. Insert a new row in SignUp table to record this change
        cursor.execute("""
            INSERT INTO SignUp (
                SignUpID, StaffID, CustomerID, SignUpDate, StoreID, MembershipLevel
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (signup_id, staff_id, customer_id, signup_date, store_id, new_membership_level))

        conn.commit()
        print(f"Membership level updated and new SignUp {signup_id} added.")

    except Exception as e:
        conn.rollback()
        print(f"Error updating membership: {e}")

    finally:
        cursor.close()
        conn.close()