from db import connect_to_db

def generate_supplier_bill(supplier_id, year):
	conn = connect_to_db()
	cursor = conn.cursor()

	# Get total cost of all transactions for the supplier for the year
	query = """
		SELECT 
			SUM(Cost) AS TotalCost
		FROM 
			SupplierTransaction
		WHERE 
			SupplierID = %s
			AND YEAR(PurchaseDate) = %s;
	"""
	cursor.execute(query, (supplier_id, int(year)))
	result = cursor.fetchone()
	if result and result[0] is not None:
		total_cost = result[0]
		print(f"SupplierID: {supplier_id}, Total Cost for Year {year}: ${total_cost:.2f}")
	else:
		print(f"No transactions found for SupplierID {supplier_id} in year {year}.")
	cursor.close()
	conn.close()