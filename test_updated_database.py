#!/usr/bin/env python3
"""
Script to test the updated database functionality
"""

import sqlite3
import os
import bcrypt

def test_frontend_database(db_path):
    """Test the frontend database functionality"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        print(f"Testing frontend database: {db_path}")
        
        # Test 1: Check if admin user exists
        cursor.execute("SELECT * FROM users WHERE email = 'admin@bossshopp.com'")
        admin_user = cursor.fetchone()
        if admin_user:
            print("✓ Admin user found")
            print(f"  Name: {admin_user['name']}")
            print(f"  Email: {admin_user['email']}")
            print(f"  Is Admin: {admin_user['is_admin']}")
            print(f"  Is Active: {admin_user['is_active']}")
        else:
            print("✗ Admin user not found")
        
        # Test 2: Check categories
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        print(f"✓ Found {len(categories)} categories:")
        for category in categories:
            print(f"  - {category['name']} ({category['slug']})")
        
        # Test 3: Check products with new columns
        cursor.execute("SELECT * FROM products LIMIT 3")
        products = cursor.fetchall()
        print(f"✓ Sample products with new columns:")
        for product in products:
            print(f"  - {product['name']}")
            print(f"    Price: R$ {product['price']}")
            print(f"    Category ID: {product['category_id']}")
            print(f"    Stock Quantity: {product['stock_quantity']}")
            print(f"    SKU: {product['sku'] or 'N/A'}")
            print(f"    Is Active: {product['is_active']}")
            print(f"    Is Featured: {product['is_featured']}")
        
        # Test 4: Check new tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('cart', 'wishlist')")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        if 'cart' in table_names:
            print("✓ Cart table exists")
        else:
            print("✗ Cart table missing")
            
        if 'wishlist' in table_names:
            print("✓ Wishlist table exists")
        else:
            print("✗ Wishlist table missing")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error testing frontend database: {e}")
        return False

def test_backend_database(db_path):
    """Test the backend database functionality"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        print(f"\nTesting backend database: {db_path}")
        
        # Test 1: Check if api_product has new columns
        cursor.execute("PRAGMA table_info(api_product)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        expected_columns = ['old_price', 'stock_quantity', 'sku', 'weight', 'dimensions', 'is_featured']
        found_columns = [col for col in expected_columns if col in column_names]
        
        print(f"✓ Found {len(found_columns)} new columns in api_product table:")
        for col in found_columns:
            print(f"  - {col}")
        
        # Test 2: Check indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
        indexes = cursor.fetchall()
        print(f"✓ Found {len(indexes)} indexes:")
        for index in indexes:
            print(f"  - {index[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error testing backend database: {e}")
        return False

def test_database_queries(db_path):
    """Test various database queries"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print(f"\nTesting database queries on: {db_path}")
        
        # Test complex query with joins
        query = """
        SELECT p.name, p.price, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = 1
        ORDER BY p.price DESC
        LIMIT 5
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("✓ Complex query with JOIN executed successfully")
        print("  Top 5 most expensive active products:")
        for row in results:
            print(f"    - {row['name']} (R$ {row['price']}) - Category: {row['category_name'] or 'N/A'}")
        
        # Test aggregation query
        cursor.execute("SELECT COUNT(*) as total_products, AVG(price) as avg_price FROM products WHERE is_active = 1")
        agg_result = cursor.fetchone()
        print(f"✓ Aggregation query executed successfully")
        print(f"  Total active products: {agg_result['total_products']}")
        print(f"  Average price: R$ {agg_result['avg_price']:.2f}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error testing database queries: {e}")
        return False

if __name__ == "__main__":
    # Test frontend database
    frontend_db = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\frontend\database.db"
    test_frontend_database(frontend_db)
    
    # Test backend database
    backend_db = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\backend\db.sqlite3"
    test_backend_database(backend_db)
    
    # Test database queries
    test_database_queries(frontend_db)
    
    print("\nDatabase testing completed!")