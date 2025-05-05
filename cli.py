import argparse

# Import handler functions from various modules

from handlers.store import (
    select_store,
	add_store,
    update_store,
    delete_store
)
from handlers.staff import (
    select_staff_by_parameter,
	add_staff,
    update_staff,
    delete_staff
)
from handlers.supplier import (
    select_supplier,
	add_supplier,
    update_supplier,
    delete_supplier
)
from handlers.supplier_transaction import (
    select_supplier_transaction,
    add_supplier_transaction,
    update_supplier_transaction,
    delete_supplier_transaction,
)
from handlers.discount import (
    select_discount,
	add_discount,
    delete_discount
)
from handlers.signup import (
    select_signup,
	add_signup,
    update_membership_via_signup
)
from handlers.merchandise import (
	select_merchandise,
    create_merchandise,
    update_merchandise,
    delete_merchandise,
    transfer_merchandise
)
from handlers.customer_transaction import (
    select_customer_transaction,
    add_customer_transaction,
    update_customer_transaction,
    delete_customer_transaction,
    return_customer_items
)
from reports.customer_activity import (
	get_customer_activity_report
)
from handlers.clubmember import (
	select_customer,
    update_customer,
    delete_customer
)
from reports.customer_growth import (
	get_customer_growth_report
)
from reports.sales import (
	get_sales_report,
    get_sales_growth_report
)
from reports.stock import (
    get_stock_report
)
from reports.reward_check import (
    generate_reward_check
)
from reports.supplier_bill import (
    generate_supplier_bill
)

# Similarly, import others as needed

# Main function for the CLI interface

def main():
    parser = argparse.ArgumentParser(description="Retail Management System CLI")
    # Optional argument to specify user type for role-based access
    parser.add_argument("--user_type", choices=["admin", "warehouse_operator", "registration_staff", "billing_staff", "manager"], required=False, help="User type")
    # Define subparsers for different operation groups
    subparsers = parser.add_subparsers(dest="group", help="Operation group")

    # === Store ===
    store = subparsers.add_parser("store")
    store_sub = store.add_subparsers(dest="action")
    for action in ["select", "add", "update", "delete"]:
        p = store_sub.add_parser(action)
        p.add_argument("--store_id", required=True)
        if action != "delete":
            p.add_argument("--address")
            p.add_argument("--phone")
            p.add_argument("--manager_id", required=False)

    # === Staff ===
    staff = subparsers.add_parser("staff")
    staff_sub = staff.add_subparsers(dest="action")
    for action in ["select", "add", "update", "delete"]:
        p = staff_sub.add_parser(action)
        if action == "select":
            p.add_argument("--staff_id", required=False)
            p.add_argument("--store_id", required=False)
        else:
            p.add_argument("--staff_id", required=True)
            
        if action not in ["delete", "select"]:
            p.add_argument("--first_name")
            p.add_argument("--last_name")
            p.add_argument("--age", type=int)
            p.add_argument("--home_address")
            p.add_argument("--job_title")
            p.add_argument("--employment_time", type=int)
            p.add_argument("--phone")
            p.add_argument("--email")
            p.add_argument("--store_id")

    # === Supplier ===
    supplier = subparsers.add_parser("supplier")
    supplier_sub = supplier.add_subparsers(dest="action")
    for action in ["select", "add", "update", "delete"]:
        p = supplier_sub.add_parser(action)
        p.add_argument("--supplier_id", required=True)
        if action != "delete":
            p.add_argument("--supplier_name")
            p.add_argument("--home_address")
            p.add_argument("--phone")
            p.add_argument("--email")
            p.add_argument("--staff_id")

    # === ClubMember ===
    member = subparsers.add_parser("member")
    member_sub = member.add_subparsers(dest="action")
    for action in ["select", "update", "delete"]:
        p = member_sub.add_parser(action)
        p.add_argument("--customer_id", required=True)
        if action == "update":
            p.add_argument("--first_name")
            p.add_argument("--last_name")
            p.add_argument("--age")
            p.add_argument("--membership_level", choices=["Silver", "Gold", "Platinum"])
            p.add_argument("--home_address")
            p.add_argument("--phone")
            p.add_argument("--email")
            p.add_argument("--active", type=bool)

    # === Merchandise ===
    merch = subparsers.add_parser("merchandise")
    merch_sub = merch.add_subparsers(dest="action")
    for action in ["select", "create", "update", "delete", "transfer"]:
        p = merch_sub.add_parser(action)
        if action == "select":
            p.add_argument("--product_id", required=False)
            p.add_argument("--store_id", required=False)
        else:
            p.add_argument("--product_id", required=True)
            p.add_argument("--store_id", required=True)
        
        if action == "transfer":
            p.add_argument("--new_store_id", required=True)
            p.add_argument("--quantity", type=int, required=True)

        if action not in ["delete", "select", "transfer"]:
            p.add_argument("--product_name")
            p.add_argument("--quantity", type=int)
            p.add_argument("--buy_price", type=float)
            p.add_argument("--market_price", type=float)
            p.add_argument("--production_date")
            p.add_argument("--expiration_date")
            p.add_argument("--supplier_id")

    # === Discount ===
    discount = subparsers.add_parser("discount")
    discount_sub = discount.add_subparsers(dest="action")
    for action in ["select", "add", "delete"]:
        p = discount_sub.add_parser(action)
        p.add_argument("--product_id", required=True)
        p.add_argument("--store_id", required=True)
        if action == "add":
            p.add_argument("--percentage", type=float, required=True)
            p.add_argument("--start_date", required=True)
            p.add_argument("--end_date", required=True)

    # === Customer Supplier Transaction ===
    cust_trans = subparsers.add_parser("customer_transaction")
    cust_trans_sub = cust_trans.add_subparsers(dest="action")
    for action in ["select", "add", "update", "delete", "return"]:
        p = cust_trans_sub.add_parser(action)
        p.add_argument("--transaction_id", required=True)
        if action not in ["delete", "return", "select"]:
            p.add_argument("--product_id", required=True)
            p.add_argument("--store_id", required=True)
            p.add_argument("--customer_id", required=True)
            p.add_argument("--staff_id")
            p.add_argument("--quantity", type=int, required=True)
            p.add_argument("--purchase_date", required=True)
        if action == "return":
            p.add_argument("--product_id", required=True)
            p.add_argument("--store_id", required=True)
            p.add_argument("--return_quantity", type=int, required=True)
        if action == "update":
            p.add_argument("--total_cost", type=float, required=True)


    # === Supplier Transaction ===
    supp_trans = subparsers.add_parser("supplier_transaction")
    supp_trans_sub = supp_trans.add_subparsers(dest="action")
    for action in ["select", "add", "update", "delete"]:
        p = supp_trans_sub.add_parser(action)
        p.add_argument("--transaction_id", required=True)
        if action not in ["delete", "select"]:
            p.add_argument("--supplier_id")
            p.add_argument("--store_id")
            p.add_argument("--product_id")
            p.add_argument("--quantity", type=int, required=True)
            p.add_argument("--purchase_date", required=True)
            p.add_argument("--cost", type=float, required=True)

    # === SignUp ===
    signup = subparsers.add_parser("signup")
    signup_sub = signup.add_subparsers(dest="action")
    for action in ["select", "add", "upgrade"]:
        p = signup_sub.add_parser(action)
        p.add_argument("--signup_id", required=True)
        if action in ["add", "upgrade"]:
            p.add_argument("--staff_id")
            p.add_argument("--customer_id", required=True)
            p.add_argument("--signup_date", required=True)
            p.add_argument("--store_id")
            p.add_argument("--membership_level", choices=["Silver", "Gold", "Platinum"], required=True)
        if action in ["add"]:
            p.add_argument("--first_name", required=True)
            p.add_argument("--last_name", required=True)
            p.add_argument("--age", type=int)
            p.add_argument("--home_address", required=True)
            p.add_argument("--phone", required=True)
            p.add_argument("--email")
            p.add_argument("--active_status", type=bool, required=True)

    # === Reports ===
    report = subparsers.add_parser("report")
    report_sub = report.add_subparsers(dest="action")

    sales = report_sub.add_parser("sales")
    sales.add_argument("--by", choices=["day", "month", "year"], required=True)
    sales.add_argument("--store_id")

    growth = report_sub.add_parser("sales_growth")
    growth.add_argument("--store_id", required=True)
    growth.add_argument("--start_date", required=True)
    growth.add_argument("--end_date", required=True)

    stock = report_sub.add_parser("stock")
    stock.add_argument("--store_id")
    stock.add_argument("--product_id")

    cust_growth = report_sub.add_parser("customer_growth")
    cust_growth.add_argument("--by", choices=["month", "year"], required=True)

    cust_activity = report_sub.add_parser("customer_activity")
    cust_activity.add_argument("--customer_id", required=True)
    cust_activity.add_argument("--start_date", required=True)
    cust_activity.add_argument("--end_date", required=True)

    reward_check = report_sub.add_parser("reward_check")
    reward_check.add_argument("--customer_id", required=True)
    reward_check.add_argument("--year", required=True)

    reward_check = report_sub.add_parser("supplier_bill")
    reward_check.add_argument("--supplier_id", required=True)
    reward_check.add_argument("--year", required=True)

    # Parse the provided arguments
    
    args = parser.parse_args()
    if not args.group:
        parser.print_help()
        return
    
    # Map (group, action) to the corresponding handler function
    
    actions = {
        ("store", "select"): lambda a: select_store(a.store_id),
        ("store", "add"): lambda a: add_store(a.store_id, a.address, a.phone, a.manager_id),
        ("store", "update"): lambda a: update_store(a.store_id, a.address, a.phone, a.manager_id),
        ("store", "delete"): lambda a: delete_store(a.store_id),

        ("staff", "select"): lambda a: select_staff_by_parameter(args.staff_id, args.store_id),
        ("staff", "add"): lambda a: add_staff(
            a.staff_id, a.first_name, a.last_name, a.age,
            a.home_address, a.job_title, a.employment_time,
            a.phone, a.email, a.store_id
        ),
        ("staff", "update"): lambda a: update_staff(
            a.staff_id, vars(a)
        ),
        ("staff", "delete"): lambda a: delete_staff(a.staff_id),

        ("supplier", "select"): lambda a: select_supplier(a.supplier_id),
        ("supplier", "add"): lambda a: add_supplier(
            a.supplier_id, a.supplier_name, a.home_address, a.phone, a.email, a.staff_id
        ),
        ("supplier", "update"): lambda a: update_supplier(
            a.supplier_id, vars(a)
        ),
        ("supplier", "delete"): lambda a: delete_supplier(a.supplier_id),

        ("supplier_transaction", "select"): lambda a: select_supplier_transaction(a.transaction_id),
        ("supplier_transaction", "add"): lambda a: add_supplier_transaction(
            a.transaction_id, a.supplier_id, a.store_id, a.product_id, a.quantity, a.purchase_date, a.cost
        ),
        ("supplier_transaction", "update"): lambda a: update_supplier_transaction(
            a.transaction_id, a.supplier_id, a.store_id, a.product_id, a.quantity, a.purchase_date, a.cost
        ),
        ("supplier_transaction", "delete"): lambda a: delete_supplier_transaction(a.transaction_id),

        ("discount", "select"): lambda a: select_discount(a.product_id, a.store_id),
        ("discount", "add"): lambda a: add_discount(
            a.product_id, a.store_id, a.percentage, a.start_date, a.end_date
        ),
        ("discount", "delete"): lambda a: delete_discount(a.product_id, a.store_id),

        ("signup", "select"): lambda a: select_signup(a.signup_id),
        ("signup", "add"): lambda a: add_signup(
            a.signup_id, a.staff_id, a.customer_id, a.signup_date, a.store_id, a.membership_level,
            a.first_name, a.last_name, a.age, a.home_address, a.phone, a.email, a.active_status
        ),
        ("signup", "upgrade"): lambda a: update_membership_via_signup(
            a.signup_id, a.staff_id, a.customer_id, a.signup_date, a.store_id, a.membership_level
        ),
        ("member", "select"): lambda a: select_customer(a.customer_id),
        ("member", "update"): lambda a: update_customer(
            a.customer_id, vars(a)
        ),
        ("member", "delete"): lambda a: delete_customer(a.customer_id),
        
("merchandise", "select"): lambda a: select_merchandise(
                a.product_id, a.store_id
            ),
            ("merchandise", "create"): lambda a: create_merchandise(
                a.product_id, a.store_id, a.product_name, a.quantity, a.buy_price, a.market_price, a.production_date, a.expiration_date, a.supplier_id
            ),
            ("merchandise", "update"): lambda a: update_merchandise(
                a.product_id, a.store_id, vars(a)
            ),
            ("merchandise", "delete"): lambda a: delete_merchandise(a.product_id, a.store_id),
            ("merchandise", "transfer"): lambda a: transfer_merchandise(a.product_id, a.store_id, a.new_store_id, a.quantity),
        
            ("customer_transaction", "select"): lambda a: select_customer_transaction(a.transaction_id),
            ("customer_transaction", "add"): lambda a: add_customer_transaction(
                a.transaction_id, a.product_id, a.store_id, a.customer_id, a.staff_id, a.quantity, a.purchase_date
            ),
            ("customer_transaction", "update"): lambda a: update_customer_transaction(
                a.transaction_id, a.product_id, a.store_id, a.customer_id, a.staff_id, a.quantity, a.purchase_date, a.total_cost
            ),
            ("customer_transaction", "delete"): lambda a: delete_customer_transaction(a.transaction_id),
            ("customer_transaction", "return"): lambda a: return_customer_items(a.transaction_id, a.product_id, a.store_id, a.return_quantity),


("report", "customer_activity"): lambda a: get_customer_activity_report(
            a.customer_id, a.start_date, a.end_date),

("report", "customer_growth"): lambda a: get_customer_growth_report(a.by),

("report", "sales"): lambda a: get_sales_report(a.by, a.store_id),
("report", "sales_growth"): lambda a: get_sales_growth_report(a.store_id, a.start_date, a.end_date),

("report", "stock"): lambda a: get_stock_report(a.product_id, a.store_id),

("report", "reward_check"): lambda a: generate_reward_check(a.customer_id, a.year),

("report", "supplier_bill"): lambda a: generate_supplier_bill(a.supplier_id, a.year),


        # ("supplier", "add"): add_supplier,
        # ("supplier", "update"): update_supplier,
        # ("supplier", "delete"): delete_supplier,

        # ("member", "add"): add_member,
        # ("member", "update"): update_member,
        # ("member", "delete"): delete_member,

        # ("merchandise", "add"): add_merchandise,
        # ("merchandise", "update"): update_merchandise,
        # ("merchandise", "delete"): delete_merchandise,

        # ("discount", "add"): add_discount,
        # ("discount", "delete"): delete_discount,

        # ("customer_transaction", "add"): customer_transaction,
        # ("supplier_transaction", "add"): supplier_transaction,

        # ("report", "sales"): sales_report,
        # ("report", "growth"): growth_report,
        # ("report", "stock"): stock_report,
        # ("report", "customer_growth"): customer_growth_report,
        # ("report", "customer_activity"): customer_activity_report,
    }
    
    # Define role-based access permissions
    
    user_permissions = {
        "admin": ["store", "staff", "supplier", "supplier_transaction", "discount", "signup", "member", "merchandise", "customer_transaction", "report"],
        "warehouse_operator": ["merchandise", "supplier_transaction"],
        "registration_staff": ["store", "staff", "signup", "member", "report"],
        "billing_staff": ["customer_transaction", "report"],
        "manager": ["store", "staff", "discount", "merchandise"],
    }
    
    # Enforce user permission based on user type
    
    if args.user_type and args.group not in user_permissions.get(args.user_type, []):
        print(f"User type '{args.user_type}' is not allowed to perform operations on '{args.group}'.")
        return
        
    # Retrieve the handler function for the command
    
    key = (args.group, args.action)

    handler = actions.get(key)

    if handler:
        # Remove group and action from arguments and execute the handler
        del args.__dict__['group']
        del args.__dict__['action']
        handler(args)
    else:
        print("Unknown command:", key)

if __name__ == "__main__":
    main()
