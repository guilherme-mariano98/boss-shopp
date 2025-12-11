#!/usr/bin/env python3
"""
Setup script for BOSS SHOPP SQLite database with admin and vendor roles
"""

import sqlite3
import bcrypt
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BossShoppDBSetup:
    """Class to setup BOSS SHOPP database with admin and vendor roles"""
    
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
    
    def execute_script(self, script_path):
        """Execute SQL script file"""
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                script = file.read()
            
            self.cursor.executescript(script)
            self.connection.commit()
            logger.info(f"Script executed successfully: {script_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error executing script {script_path}: {e}")
            self.connection.rollback()
            return False
        except FileNotFoundError:
            logger.error(f"Script file not found: {script_path}")
            return False
    
    def create_admin_user(self, email="admin@bossshopp.com", password="admin123", name="Administrador"):
        """Create default admin user"""
        try:
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # First try to update existing user
            query = """
            UPDATE users SET name = ?, password = ?, is_admin = 1 
            WHERE email = ?
            """
            
            result = self.cursor.execute(query, (name, hashed_password, email))
            
            # If no rows were updated, insert new user
            if result.rowcount == 0:
                query = """
                INSERT INTO users (name, email, password, is_admin, city, state, country)
                VALUES (?, ?, ?, 1, ?, ?, ?)
                """
                
                self.cursor.execute(query, (
                    name, email, hashed_password,
                    "São Paulo", "SP", "Brasil"
                ))
            
            self.connection.commit()
            logger.info(f"Admin user created/updated: {email}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating admin user: {e}")
            self.connection.rollback()
            return False
    
    def create_vendor_user(self, email="vendor@bossshopp.com", password="vendor123", name="Vendedor Padrão"):
        """Create default vendor user"""
        try:
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # First try to update existing user
            query = """
            UPDATE users SET name = ?, password = ?, is_vendor = 1 
            WHERE email = ?
            """
            
            result = self.cursor.execute(query, (name, hashed_password, email))
            
            # If no rows were updated, insert new user
            if result.rowcount == 0:
                query = """
                INSERT INTO users (name, email, password, is_admin, is_vendor, city, state, country)
                VALUES (?, ?, ?, 0, 1, ?, ?, ?)
                """
                
                self.cursor.execute(query, (
                    name, email, hashed_password,
                    "São Paulo", "SP", "Brasil"
                ))
            
            self.connection.commit()
            logger.info(f"Vendor user created/updated: {email}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating vendor user: {e}")
            self.connection.rollback()
            return False
    
    def setup_database(self):
        """Setup complete database with admin and vendor roles"""
        # Connect to database
        if not self.connect():
            return False
        
        try:
            # Execute the schema script
            schema_path = os.path.join(os.path.dirname(__file__), "admin_vendor_sqlite_schema.sql")
            if not self.execute_script(schema_path):
                return False
            
            # Create default admin user
            if not self.create_admin_user():
                return False
            
            # Create default vendor user
            if not self.create_vendor_user():
                return False
            
            logger.info("Database setup completed successfully!")
            return True
        except Exception as e:
            logger.error(f"Error during database setup: {e}")
            return False
        finally:
            self.disconnect()
    
    def test_connection(self):
        """Test database connection and basic queries"""
        if not self.connect():
            return False
        
        try:
            # Test users table
            self.cursor.execute("SELECT COUNT(*) as count FROM users")
            users_count = self.cursor.fetchone()['count']
            logger.info(f"Users table has {users_count} records")
            
            # Test categories table
            self.cursor.execute("SELECT COUNT(*) as count FROM categories")
            categories_count = self.cursor.fetchone()['count']
            logger.info(f"Categories table has {categories_count} records")
            
            # Test products table
            self.cursor.execute("SELECT COUNT(*) as count FROM products")
            products_count = self.cursor.fetchone()['count']
            logger.info(f"Products table has {products_count} records")
            
            # Test admin user
            self.cursor.execute("SELECT * FROM users WHERE is_admin = 1 LIMIT 1")
            admin_user = self.cursor.fetchone()
            if admin_user:
                logger.info(f"Admin user found: {admin_user['name']} ({admin_user['email']})")
            
            # Test vendor user
            self.cursor.execute("SELECT * FROM users WHERE is_vendor = 1 LIMIT 1")
            vendor_user = self.cursor.fetchone()
            if vendor_user:
                logger.info(f"Vendor user found: {vendor_user['name']} ({vendor_user['email']})")
            
            logger.info("Connection test completed successfully!")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error during connection test: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """Main function to setup database"""
    print("BOSS SHOPP Database Setup with Admin and Vendor Roles")
    print("=" * 50)
    
    # Create database setup instance
    db_setup = BossShoppDBSetup("bossshopp_admin_vendor.db")
    
    # Setup database
    print("Setting up database...")
    if db_setup.setup_database():
        print("✓ Database setup completed successfully!")
        
        # Test connection
        print("Testing database connection...")
        if db_setup.test_connection():
            print("✓ Database connection test passed!")
            print(f"\nDatabase file created: {os.path.abspath('bossshopp_admin_vendor.db')}")
            print("\nDefault users:")
            print("- Admin: admin@bossshopp.com / admin123")
            print("- Vendor: vendor@bossshopp.com / vendor123")
        else:
            print("✗ Database connection test failed!")
    else:
        print("✗ Database setup failed!")

if __name__ == "__main__":
    main()