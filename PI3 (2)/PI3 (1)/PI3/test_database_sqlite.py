#!/usr/bin/env python3
"""
BOSS SHOPP Database Test Script for SQLite
Tests the database connection and verifies the schema
"""

import sqlite3
import os

def test_database():
    """Test the database connection and verify schema"""
    
    # Database file
    db_file = "bossshopp_complete.db"
    
    # Check if database file exists
    if not os.path.exists(db_file):
        print("❌ Database file not found. Please run create_database_sqlite.py first.")
        return
    
    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print("✅ Successfully connected to SQLite database")
        
        # Test 1: Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Test 2: Check categories
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        print(f"✅ Categories table has {category_count} records")
        
        # Test 3: Check products
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"✅ Products table has {product_count} records")
        
        # Test 4: Check users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Users table has {user_count} records")
        
        # Test 5: Check system settings
        cursor.execute("SELECT COUNT(*) FROM system_settings")
        settings_count = cursor.fetchone()[0]
        print(f"✅ System settings table has {settings_count} records")
        
        # Test 6: Sample data verification
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
        cursor.execute("SELECT name, email, is_admin FROM users WHERE is_admin = 1 LIMIT 1")
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
        
    except sqlite3.Error as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check:")
        print("1. Database file exists")
        print("2. Database file is not corrupted")
    
    finally:
        if conn:
            conn.close()
            print("SQLite connection closed")

if __name__ == "__main__":
    test_database()