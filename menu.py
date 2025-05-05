from handlers.store import add_store, update_store, delete_store
from handlers.staff import add_staff, update_staff, delete_staff
from handlers.supplier import add_supplier, update_supplier, delete_supplier
from handlers.clubmember import update_customer, delete_customer
from handlers.merchandise import create_merchandise, update_merchandise, delete_merchandise
from handlers.customer_transaction import (
    add_customer_transaction,
    update_customer_transaction,
    delete_customer_transaction,
    return_customer_items,
)
from handlers.supplier_transaction import (
    add_supplier_transaction,
    update_supplier_transaction,
    delete_supplier_transaction,
)
from handlers.discount import add_discount, delete_discount
from handlers.signup import add_signup, update_membership_via_signup

user_type = None
permissions = {
    "admin": ["store", "staff", "supplier", "clubmember", "merchandise", "customer_transaction", "supplier_transaction", "discount", "signup", "return"],
    "warehouse_operator": ["merchandise", "supplier_transaction"],
    "registration_staff": ["store", "staff", "signup", "clubmember"],
    "billing_staff": ["customer_transaction", "return"],
    "manager": ["store", "staff", "discount", "merchandise"]
}
from reports.sales import get_sales_growth_report, get_sales_report
from reports.stock import get_stock_report
from reports.customer_growth import get_customer_growth_report
from reports.customer_activity import get_customer_activity_report
from reports.reward_check import generate_reward_check
from reports.supplier_bill import generate_supplier_bill

# Main menu providing access to all system modules

def main_menu():
    global user_type
    print("\n=== Welcome to WolfWR Retail Management System ===\n")
    print("Please select your role:")
    print("1. Admin")
    print("2. Warehouse Operator")
    print("3. Registration Staff")
    print("4. Billing Staff")
    print("5. Manager")

    role_choice = input("Enter your role number: ")
    role_map = {
        "1": "admin",
        "2": "warehouse_operator",
        "3": "registration_staff",
        "4": "billing_staff",
        "5": "manager"
    }
    user_type = role_map.get(role_choice)
    if not user_type:
        print("Invalid role selected.")
        return

    while True:
        print("\n=== WolfWR Retail Management System ===\n")
        print("1. Store")
        print("2. Staff")
        print("3. Supplier")
        print("4. Club Member")
        print("5. Merchandise")
        print("6. Customer Transaction")
        print("7. Supplier Transaction")
        print("8. Discount")
        print("9. Signup")
        print("10. Reports")
        print("11. Return Item")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1" and "store" in permissions[user_type]: store_menu()
        elif choice == "2" and "staff" in permissions[user_type]: staff_menu()
        elif choice == "3" and "supplier" in permissions[user_type]: supplier_menu()
        elif choice == "4" and "clubmember" in permissions[user_type]: clubmember_menu()
        elif choice == "5" and "merchandise" in permissions[user_type]: merchandise_menu()
        elif choice == "6" and "customer_transaction" in permissions[user_type]: customer_transaction_menu()
        elif choice == "7" and "supplier_transaction" in permissions[user_type]: supplier_transaction_menu()
        elif choice == "8" and "discount" in permissions[user_type]: discount_menu()
        elif choice == "9" and "signup" in permissions[user_type]: signup_menu()
        elif choice == "10" and "return" in permissions[user_type]: report_menu()
        elif choice == "11": return_menu()
        elif choice == "0": break
        else: print("\nYou do not have permission for this operation or invalid choice.\n")
# Store submenu for add, update, and delete operations

def store_menu():
    print("\n-- Store --\n")
    choice = input("\n1. Add 2. Update 3. Delete: ")
    sid = input("\nStore ID: ")
    if choice == "1": add_store(sid, input("\nAddress: "), input("\nPhone: "), input("\nManager ID: "))
    elif choice == "2": update_store(sid, input("\nNew Address: "), input("\nNew Phone: "), input("\nNew Manager ID: "))
    elif choice == "3": delete_store(sid)

# Staff submenu for managing staff records

def staff_menu():
    print("\n-- Staff --")
    choice = input("\n1. Add 2. Update 3. Delete: ")
    sid = input("\nStaff ID: ")
    if choice in ["1", "2"]:
        fname = input("\nFirst Name: ")
        lname = input("\nLast Name: ")
        age = int(input("\nAge: "))
        addr = input("\nHome Address: ")
        title = input("\nJob Title: ")
        emp_time = int(input("\nEmployment Time: "))
        phone = input("\nPhone: ")
        email = input("\nEmail: ")
        store_id = input("\nStore ID: ")
        if choice == "1":
            add_staff(sid, fname, lname, age, addr, title, emp_time, phone, email, store_id)
        else:
            update_staff(sid, fname, lname, age, addr, title, emp_time, phone, email, store_id)
    elif choice == "3": delete_staff(sid)

# Supplier submenu for add, update, and delete operations

def supplier_menu():
    print("\n-- Supplier --")
    choice = input("\n1. Add 2. Update 3. Delete: ")
    spid = input("\nSupplier ID: ")
    if choice in ["1", "2"]:
        name = input("\nName: ")
        addr = input("\nAddress: ")
        phone = input("\nPhone: ")
        email = input("\nEmail: ")
        staff_id = input("\nStaff ID: ")
        if choice == "1":
            add_supplier(spid, name, addr, phone, email, staff_id)
        else:
            update_supplier(spid, name, addr, phone, email, staff_id)
    elif choice == "3": delete_supplier(spid)

# Club Member submenu for updating and deleting records

def clubmember_menu():
    print("\n-- Club Member --")
    choice = input("\n1. Update 2. Delete: ")
    cid = input("\nCustomer ID: ")
    if choice == "1":
        fname = input("\nFirst Name: ")
        lname = input("\nLast Name: ")
        level = input("\nLevel (Silver/Gold/Platinum): ")
        addr = input("\nHome Address: ")
        phone = input("\nPhone: ")
        email = input("\nEmail: ")
        active = input("\nActive (True/False): ") == "True"
        update_customer(cid, fname, lname, level, addr, phone, email, active)
    elif choice == "2": delete_customer(cid)

# Merchandise submenu for create, update, and delete operations

def merchandise_menu():
    print("\n-- Merchandise --")
    choice = input("\n1. Create 2. Update 3. Delete: ")
    pid = input("\nProduct ID: ")
    store = input("\nStore ID: ")
    if choice == "1":
        create_merchandise(pid, store, input("\nName: "), int(input("\nQty: ")), float(input("\nBuy Price: ")), float(input("\nMarket Price: ")), input("\nProd Date: "), input("\nExp Date: "), input("\nSupplier ID: "))
    elif choice == "2":
        args = {
            "product_name": input("\nName: "),
            "quantity": int(input("\nQty: ")),
            "market_price": float(input("\nMarket Price: ")),
            "supplier_id": input("\nSupplier ID: ")
        }
        update_merchandise(pid, store, args)
    elif choice == "3": delete_merchandise(pid, store)

# Customer Transaction submenu for add, update, and delete operations

def customer_transaction_menu():
    print("\n-- Customer Transaction --")
    choice = input("\n1. Add 2. Update 3. Delete: ")
    tid = input("\nTransaction ID: ")
    if choice in ["1", "2"]:
        pid = input("\nProduct ID: ")
        store = input("\nStore ID: ")
        cid = input("\nCustomer ID: ")
        sid = input("\nStaff ID: ")
        qty = int(input("\nQuantity: "))
        date = input("\nPurchase Date: ")
        cost = float(input("\nTotal Cost: "))
        if choice == "1":
            add_customer_transaction(tid, pid, store, cid, sid, qty, date)
        else:
            update_customer_transaction(tid, pid, store, cid, sid, qty, date, cost)
    elif choice == "3": delete_customer_transaction(tid)

# Supplier Transaction submenu for add, update, and delete operations

def supplier_transaction_menu():
    print("\n-- Supplier Transaction --")
    choice = input("\n1. Add 2. Update 3. Delete: ")
    tid = input("\nTransaction ID: ")
    if choice in ["1", "2"]:
        spid = input("\nSupplier ID: ")
        store = input("\nStore ID: ")
        pid = input("\nProduct ID: ")
        qty = int(input("\nQuantity: "))
        date = input("\nPurchase Date: ")
        cost = float(input("\nCost: "))
        if choice == "1":
            add_supplier_transaction(tid, spid, store, pid, qty, date, cost)
        else:
            update_supplier_transaction(tid, spid, store, pid, qty, date, cost)
    elif choice == "3": delete_supplier_transaction(tid)

# Discount submenu for adding and deleting discounts

def discount_menu():
    print("\n-- Discount --")
    choice = input("\n1. Add 2. Delete: ")
    pid = input("\nProduct ID: ")
    store = input("\nStore ID: ")
    if choice == "1":
        percent = float(input("\nDiscount %: "))
        start = input("\nStart Date: ")
        end = input("\nEnd Date: ")
        add_discount(pid, store, percent, start, end)
    elif choice == "2": delete_discount(pid, store)

# Signup submenu for add and upgrade operations

def signup_menu():
    print("\n-- Sign Up --")
    choice = input("\n1. Add 2. Upgrade: ")
    sid = input("\nSignup ID: ")
    staff = input("\nStaff ID: ")
    cid = input("\nCustomer ID: ")
    date = input("\nSignup Date: ")
    store = input("\nStore ID: ")
    level = input("\nLevel (Silver/Gold/Platinum): ")
    if choice == "1":
        fname = input("\nFirst Name: ")
        lname = input("\nLast Name: ")
        age = int(input("\nAge: "))
        addr = input("\nAddress: ")
        phone = input("\nPhone: ")
        email = input("\nEmail: ")
        active = input("\nActive (True/False): ") == "True"
        add_signup(sid, staff, cid, date, store, level, fname, lname, age, addr, phone, email, active)
    elif choice == "2":
        update_membership_via_signup(sid, staff, cid, date, store, level)

# Report submenu for various reports
    
def report_menu():
    print("\n-- Reports --")
    print("1. Sales Report")
    print("2. Sales Growth Report")
    print("3. Stock Report")
    print("4. Customer Growth Report")
    print("5. Customer Activity Report")
    print("6. Reward Check")
    print("7. Supplier Bill Report")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        report_sales()
    elif choice == "2":
        report_sales_growth()
    elif choice == "3":
        report_stock()
    elif choice == "4":
        report_customer_growth()
    elif choice == "5":
        report_customer_activity()
    elif choice == "6":
        report_reward_check()
    elif choice == "7":
        report_supplier_bill()
    else:
        print("\nInvalid choice!\n")

# Functions to call individual report modules

def report_sales():
    by = input("\nReport by (day/month/year): ")
    store_id = input("\nEnter Store ID: ")
    # Call the corresponding report function from cli.py
    get_sales_report(by, store_id)

def report_sales_growth():
    store_id = input("\nEnter Store ID: ")
    start_date = input("\nStart Date (YYYY-MM-DD): ")
    end_date = input("\nEnd Date (YYYY-MM-DD): ")
    # Call the corresponding report function from cli.py
    get_sales_growth_report(store_id, start_date, end_date)

def report_stock():
    store_id = input("\nEnter Store ID: ")
    product_id = input("\nEnter Product ID: ")
    # Call the corresponding report function from cli.py
    get_stock_report(product_id, store_id)

def report_customer_growth():
    by = input("\nGrowth by (month/year): ")
    # Call the corresponding report function from cli.py
    get_customer_growth_report(by)

def report_customer_activity():
    customer_id = input("\nEnter Customer ID: ")
    start_date = input("\nStart Date (YYYY-MM-DD): ")
    end_date = input("\nEnd Date (YYYY-MM-DD): ")
    # Call the corresponding report function from cli.py
    get_customer_activity_report(customer_id, start_date, end_date)

def report_reward_check():
    customer_id = input("\nEnter Customer ID: ")
    year = input("\nEnter Year: ")
    # Call the corresponding report function from cli.py
    generate_reward_check(customer_id, year)

def report_supplier_bill():
    supplier_id = input("\nEnter Supplier ID: ")
    year = input("\nEnter Year: ")
    # Call the corresponding report function from cli.py
    generate_supplier_bill(supplier_id, year)

# Return submenu for processing returns
def return_menu():
    print("\n-- Return Items --")
    tid = input("Transaction ID to return from: ")
    pid = input("Product ID: ")
    store = input("Store ID: ")
    qty = int(input("Return Quantity: "))
    return_customer_items(tid, pid, store, qty)

# Start the menu-driven application

if __name__ == "__main__":
    main_menu()