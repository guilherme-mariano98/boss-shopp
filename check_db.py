import sqlite3

# Connect to the database
conn = sqlite3.connect('bossshopp_admin_vendor.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check users
print("Users in database:")
cursor.execute("SELECT id, name, email, is_admin, is_vendor FROM users;")
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Admin: {user['is_admin']}, Vendor: {user['is_vendor']}")

# Check if the vendor flag is being set correctly by querying specifically
print("\nChecking vendor users specifically:")
cursor.execute("SELECT id, name, email FROM users WHERE is_vendor = 1;")
vendors = cursor.fetchall()
if vendors:
    for vendor in vendors:
        print(f"  Vendor: {vendor['name']} ({vendor['email']})")
else:
    print("  No users with is_vendor = 1 found")

# Check products and their vendors
print("\nProducts and their vendors:")
cursor.execute("""
    SELECT p.id, p.name, u.name as vendor_name, p.vendor_id, u.id as user_id
    FROM products p 
    LEFT JOIN users u ON p.vendor_id = u.id 
    LIMIT 10;
""")
products = cursor.fetchall()
for product in products:
    print(f"  Product: {product['name']}, Vendor ID: {product['vendor_id']}, User ID: {product['user_id']}, Vendor: {product['vendor_name']}")

# Check the actual insert query results
print("\nChecking if vendor user exists in database:")
cursor.execute("SELECT * FROM users WHERE email = 'vendor@bossshopp.com';")
vendor_user = cursor.fetchone()
if vendor_user:
    print(f"  Vendor user found: {vendor_user['name']}")
    print(f"  is_admin: {vendor_user['is_admin']}, is_vendor: {vendor_user['is_vendor']}")
else:
    print("  Vendor user not found")

conn.close()