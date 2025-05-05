from db import connect_to_db

def generate_reward_check(customer_id, year):
    conn = connect_to_db()
    cursor = conn.cursor()
    # Compile a list of ranges that the member was a Platinum customer
    query = """
        SELECT 
            SignUpDate, MembershipLevel
        FROM 
            SignUp
        WHERE 
            CustomerID = %s
            AND YEAR(SignUpDate) BETWEEN %s AND %s
        ORDER BY 
            SignUpDate;
    """
    cursor.execute(query, (customer_id, int(year) - 1, year))
    membership_history = cursor.fetchall()

    platinum_ranges = []
    current_start_date = None

    for record in membership_history:
        sign_up_date, membership_level = record
        sign_up_date = sign_up_date.strftime('%Y-%m-%d')
        if membership_level == 'Platinum':
            if current_start_date is None:
                current_start_date = sign_up_date
        else:
            if current_start_date is not None:
                platinum_ranges.append((current_start_date, sign_up_date))
                current_start_date = None

    if current_start_date is not None:
        # If still Platinum at the end of the year, assume the range ends at year-end
        year_end_date = f"{year}-12-31"
        platinum_ranges.append((current_start_date, year_end_date))

    #print(f"CustomerID: {customer_id}, Platinum Membership Ranges: {platinum_ranges}")
    total_cashback = 0.0
    for range in platinum_ranges:
        platinum_start_date = range[0]
        platinum_end_date = range[1]
        cursor.execute("""
            SELECT 
                cm.CustomerID,
                CONCAT(cm.FirstName, ' ', cm.LastName) AS CustomerName,
                SUM(ct.TotalCost) * 0.02 AS CashbackReward
            FROM 
                ClubMember cm
            JOIN 
                CustomerTransaction ct ON cm.CustomerID = ct.CustomerID
            WHERE 
                cm.CustomerID = %s
                AND ct.PurchaseDate BETWEEN %s AND %s
                AND YEAR(ct.PurchaseDate) = %s
            GROUP BY 
                cm.CustomerID, cm.FirstName, cm.LastName
            HAVING 
                SUM(ct.TotalCost) > 0;
        """, (customer_id, platinum_start_date, platinum_end_date, year))
        results = cursor.fetchone()
        if results:
            total_cashback += float(results[2])

    print(f"CustomerID: {customer_id}, Cashback Reward: ${total_cashback:.2f}")
    cursor.close()
    conn.close()