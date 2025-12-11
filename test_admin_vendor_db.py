#!/usr/bin/env python3
"""
Test script for BOSS SHOPP SQLite database with admin and vendor roles
"""

import sqlite3
import bcrypt
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BossShoppDBTester:
    """Class to test BOSS SHOPP database with admin and vendor roles"""
    
    def __init__(self, db_path="bossshopp_admin_vendor.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to database: {self.db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def test_users_table(self):
        """Test users table"""
        try:
            # Count total users
            self.cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = self.cursor.fetchone()['count']
            print(f"Total users: {total_users}")
            
            # Count admin users
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1")
            admin_users = self.cursor.fetchone()['count']
            print(f"Admin users: {admin_users}")
            
            # Count vendor users
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_vendor = 1")
            vendor_users = self.cursor.fetchone()['count']
            print(f"Vendor users: {vendor_users}")
            
            # Get sample users
            self.cursor.execute("SELECT id, name, email, is_admin, is_vendor FROM users LIMIT 5")
            users = self.cursor.fetchall()
            print("\nSample users:")
            for user in users:
                print(f"  - {user['name']} ({user['email']}) - Admin: {bool(user['is_admin'])}, Vendor: {bool(user['is_vendor'])}")
            
            return True
        except sqlite3.Error as e:
            logger.error(f"Error testing users table: {e}")
            return False
    
    def test_products_table(self):
        """Test products table"""
        try:
            # Count total products
            self.cursor.execute("SELECT COUNT(*) as count FROM products")
            total_products = self.cursor.fetchone()['count']
            print(f"\nTotal products: {total_products}")
            
            # Count products by vendor
            self.cursor.execute("""
                SELECT u.name as vendor_name, COUNT(p.id) as product_count
                FROM users u
                LEFT JOIN products p ON u.id = p.vendor_id
                WHERE u.is_vendor = 1
                GROUP BY u.id, u.name
            """)
            vendor_products = self.cursor.fetchall()
            print("\nProducts by vendor:")
            for vendor in vendor_products:
                print(f"  - {vendor['vendor_name']}: {vendor['product_count']} products")
            
            return True
        except sqlite3.Error as e:
            logger.error(f"Error testing products table: {e}")
            return False
    
    def test_categories_table(self):
        """Test categories table"""
        try:
            # Count total categories
            self.cursor.execute("SELECT COUNT(*) as count FROM categories")
            total_categories = self.cursor.fetchone()['count']
            print(f"\nTotal categories: {total_categories}")
            
            # List categories
            self.cursor.execute("SELECT id, name, slug FROM categories ORDER BY sort_order")
            categories = self.cursor.fetchall()
            print("\nCategories:")
            for category in categories:
                print(f"  - {category['name']} ({category['slug']})")
            
            return True
        except sqlite3.Error as e:
            logger.error(f"Error testing categories table: {e}")
            return False
    
    def test_views(self):
        """Test database views"""
        try:
            # Test products_with_category view
            self.cursor.execute("SELECT COUNT(*) as count FROM products_with_category")
            products_with_category = self.cursor.fetchone()['count']
            print(f"\nProducts with category view: {products_with_category} records")
            
            # Test vendor_products view
            self.cursor.execute("SELECT COUNT(*) as count FROM vendor_products")
            vendor_products = self.cursor.fetchone()['count']
            print(f"Vendor products view: {vendor_products} records")
            
            # Test vendor_statistics view
            self.cursor.execute("SELECT COUNT(*) as count FROM vendor_statistics")
            vendor_statistics = self.cursor.fetchone()['count']
            print(f"Vendor statistics view: {vendor_statistics} records")
            
            return True
        except sqlite3.Error as e:
            logger.error(f"Error testing views: {e}")
            return False
    
    def authenticate_user(self, email, password):
        """Authenticate user (simplified for testing)"""
        try:
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = self.cursor.fetchone()
            
            if user:
                # In a real implementation, we would check the password hash
                # For this test, we'll just return the user if email exists
                print(f"\nAuthenticated user: {user['name']} ({user['email']})")
                print(f"Roles - Admin: {bool(user['is_admin'])}, Vendor: {bool(user['is_vendor'])}")
                return dict(user)
            else:
                print(f"\nUser not found: {email}")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    def run_all_tests(self):
        """Run all database tests"""
        print("BOSS SHOPP Database Test")
        print("=" * 30)
        
        # Connect to database
        if not self.connect():
            return False
        
        try:
            # Run individual tests
            print("\n1. Testing Users Table:")
            if not self.test_users_table():
                return False
            
            print("\n2. Testing Products Table:")
            if not self.test_products_table():
                return False
            
            print("\n3. Testing Categories Table:")
            if not self.test_categories_table():
                return False
            
            print("\n4. Testing Views:")
            if not self.test_views():
                return False
            
            print("\n5. Testing Authentication:")
            self.authenticate_user("admin@bossshopp.com", "admin123")
            self.authenticate_user("vendor@bossshopp.com", "vendor123")
            
            print("\n" + "=" * 30)
            print("All tests completed successfully!")
            return True
        except Exception as e:
            logger.error(f"Error during tests: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """Main function to run database tests"""
    print("BOSS SHOPP Database Test with Admin and Vendor Roles")
    print("=" * 50)
    
    # Check if database file exists
    db_file = "bossshopp_admin_vendor.db"
    if not os.path.exists(db_file):
        print(f"Database file not found: {db_file}")
        print("Please run setup_admin_vendor_db.py first!")
        return
    
    # Create database tester instance
    db_tester = BossShoppDBTester(db_file)
    
    # Run tests
    if db_tester.run_all_tests():
        print("\n✓ All database tests passed!")
    else:
        print("\n✗ Some database tests failed!")

if __name__ == "__main__":
    main()