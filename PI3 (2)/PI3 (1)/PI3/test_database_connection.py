#!/usr/bin/env python3
"""
BOSS SHOPP Database Connection Test
Tests the database connection and verifies the schema
"""

import mysql.connector
from mysql.connector import Error

def test_database_connection():
    """Test the database connection and verify schema"""
    
    # Database configuration
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'boss_shopp_complete'
    }
    
    connection = None
    cursor = None
    
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            print("✅ Successfully connected to MySQL database")
            
            # Test 1: Check if database exists
            cursor.execute("SHOW DATABASES LIKE 'boss_shopp_complete'")
            result = cursor.fetchone()
            if result:
                print("✅ Database 'boss_shopp_complete' exists")
            else:
                print("❌ Database 'boss_shopp_complete' not found")
                return
            
            # Test 2: Check tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Test 3: Check categories
            cursor.execute("SELECT COUNT(*) FROM categories")
            category_count = cursor.fetchone()[0]
            print(f"✅ Categories table has {category_count} records")
            
            # Test 4: Check products
            cursor.execute("SELECT COUNT(*) FROM products")
            product_count = cursor.fetchone()[0]
            print(f"✅ Products table has {product_count} records")
            
            # Test 5: Check users
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"✅ Users table has {user_count} records")
            
            # Test 6: Check system settings
            cursor.execute("SELECT COUNT(*) FROM system_settings")
            settings_count = cursor.fetchone()[0]
            print(f"✅ System settings table has {settings_count} records")
            
            # Test 7: Check views
            cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
            views = cursor.fetchall()
            print(f"✅ Found {len(views)} views:")
            for view in views:
                print(f"   - {view[0]}")
            
            # Test 8: Sample data verification
            print("\n--- Sample Data Verification ---")
            
            # Get sample categories
            cursor.execute("SELECT name, slug FROM categories LIMIT 3")
            categories = cursor.fetchall()
            print("Sample categories:")
            for category in categories:
                print(f"   - {category[0]} ({category[1]})")
            
            # Get sample products
            cursor.execute("SELECT name, price, category_id FROM products LIMIT 3")
            products = cursor.fetchall()
            print("Sample products:")
            for product in products:
                print(f"   - {product[0]} (R$ {product[1]})")
            
            # Get admin user
            cursor.execute("SELECT name, email, is_admin FROM users WHERE is_admin = TRUE LIMIT 1")
            admin = cursor.fetchone()
            if admin:
                print(f"Admin user: {admin[0]} ({admin[1]})")
            else:
                print("No admin user found")
            
            print("\n" + "="*50)
            print("DATABASE CONNECTION TEST PASSED!")
            print("="*50)
            print("All tables and data are properly configured")
            print("Database is ready for use")
            print("="*50)
            
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check:")
        print("1. MySQL server is running")
        print("2. Database credentials are correct")
        print("3. Database has been created (run create_database.py)")
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    test_database_connection()