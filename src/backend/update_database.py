#!/usr/bin/env python3
"""
Script to update and synchronize the SQLite databases
"""

import sqlite3
import os
import bcrypt
from datetime import datetime

def update_frontend_database(db_path):
    """Update the frontend database with additional features"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"Updating frontend database: {db_path}")
        
        # Add is_active column to users table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1")
            print("Added is_active column to users table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("is_active column already exists in users table")
            else:
                print(f"Error adding is_active column: {e}")
        
        # Add is_admin column to users table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            print("Added is_admin column to users table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("is_admin column already exists in users table")
            else:
                print(f"Error adding is_admin column: {e}")
        
        # Add more columns to products table if they don't exist
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN old_price REAL")
            print("Added old_price column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("old_price column already exists in products table")
            else:
                print(f"Error adding old_price column: {e}")
        
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN stock_quantity INTEGER DEFAULT 0")
            print("Added stock_quantity column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("stock_quantity column already exists in products table")
            else:
                print(f"Error adding stock_quantity column: {e}")
        
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN sku TEXT")
            print("Added sku column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("sku column already exists in products table")
            else:
                print(f"Error adding sku column: {e}")
        
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN weight REAL")
            print("Added weight column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("weight column already exists in products table")
            else:
                print(f"Error adding weight column: {e}")
        
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN dimensions TEXT")
            print("Added dimensions column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("dimensions column already exists in products table")
            else:
                print(f"Error adding dimensions column: {e}")
        
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN is_active INTEGER DEFAULT 1")
            print("Added is_active column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("is_active column already exists in products table")
            else:
                print(f"Error adding is_active column: {e}")
        
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN is_featured INTEGER DEFAULT 0")
            print("Added is_featured column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("is_featured column already exists in products table")
            else:
                print(f"Error adding is_featured column: {e}")
        
        # Create categories table if it doesn't exist
        try:
            cursor.execute("""
                CREATE TABLE categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    slug TEXT UNIQUE NOT NULL,
                    description TEXT,
                    image_url TEXT,
                    is_active INTEGER DEFAULT 1,
                    sort_order INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Created categories table")
            
            # Insert default categories
            categories = [
                ('Moda', 'moda', 'Roupas e acessórios de moda'),
                ('Eletrônicos', 'eletronicos', 'Dispositivos eletrônicos e gadgets'),
                ('Casa', 'casa', 'Produtos para casa e decoração'),
                ('Games', 'games', 'Jogos e consoles'),
                ('Esportes', 'esportes', 'Artigos esportivos e fitness'),
                ('Infantil', 'infantil', 'Produtos para crianças')
            ]
            
            cursor.executemany(
                "INSERT OR IGNORE INTO categories (name, slug, description) VALUES (?, ?, ?)",
                categories
            )
            print("Inserted default categories")
            
        except sqlite3.OperationalError as e:
            if "table categories already exists" in str(e):
                print("Categories table already exists")
            else:
                print(f"Error creating categories table: {e}")
        
        # Add category_id column to products table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN category_id INTEGER REFERENCES categories(id)")
            print("Added category_id column to products table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("category_id column already exists in products table")
            else:
                print(f"Error adding category_id column: {e}")
        
        # Update existing products with category_id if not set
        cursor.execute("UPDATE products SET category_id = (SELECT id FROM categories WHERE categories.slug = products.category) WHERE category_id IS NULL AND category IS NOT NULL")
        updated_rows = cursor.rowcount
        if updated_rows > 0:
            print(f"Updated {updated_rows} products with category_id")
        
        # Create indexes for better performance
        try:
            cursor.execute("CREATE INDEX idx_products_category ON products(category)")
            print("Created index on products.category")
        except sqlite3.OperationalError as e:
            if "index idx_products_category already exists" in str(e):
                print("Index idx_products_category already exists")
            else:
                print(f"Error creating index: {e}")
        
        try:
            cursor.execute("CREATE INDEX idx_products_category_id ON products(category_id)")
            print("Created index on products.category_id")
        except sqlite3.OperationalError as e:
            if "index idx_products_category_id already exists" in str(e):
                print("Index idx_products_category_id already exists")
            else:
                print(f"Error creating index: {e}")
        
        try:
            cursor.execute("CREATE INDEX idx_users_email ON users(email)")
            print("Created index on users.email")
        except sqlite3.OperationalError as e:
            if "index idx_users_email already exists" in str(e):
                print("Index idx_users_email already exists")
            else:
                print(f"Error creating index: {e}")
        
        # Create cart table
        try:
            cursor.execute("""
                CREATE TABLE cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id),
                    product_id INTEGER REFERENCES products(id),
                    quantity INTEGER NOT NULL DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Created cart table")
        except sqlite3.OperationalError as e:
            if "table cart already exists" in str(e):
                print("Cart table already exists")
            else:
                print(f"Error creating cart table: {e}")
        
        # Create wishlist table
        try:
            cursor.execute("""
                CREATE TABLE wishlist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id),
                    product_id INTEGER REFERENCES products(id),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Created wishlist table")
        except sqlite3.OperationalError as e:
            if "table wishlist already exists" in str(e):
                print("Wishlist table already exists")
            else:
                print(f"Error creating wishlist table: {e}")
        
        # Commit changes
        conn.commit()
        conn.close()
        print("Frontend database update completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error updating frontend database: {e}")
        return False

def update_backend_database(db_path):
    """Update the backend database with additional features"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"Updating backend database: {db_path}")
        
        # Add indexes for better performance
        try:
            cursor.execute("CREATE INDEX idx_api_product_category ON api_product(category_id)")
            print("Created index on api_product.category_id")
        except sqlite3.OperationalError as e:
            if "index idx_api_product_category already exists" in str(e):
                print("Index idx_api_product_category already exists")
            else:
                print(f"Error creating index: {e}")
        
        try:
            cursor.execute("CREATE INDEX idx_api_order_user ON api_order(user_id)")
            print("Created index on api_order.user_id")
        except sqlite3.OperationalError as e:
            if "index idx_api_order_user already exists" in str(e):
                print("Index idx_api_order_user already exists")
            else:
                print(f"Error creating index: {e}")
        
        # Add additional columns to api_product table if they don't exist
        try:
            cursor.execute("ALTER TABLE api_product ADD COLUMN old_price DECIMAL")
            print("Added old_price column to api_product table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("old_price column already exists in api_product table")
            else:
                print(f"Error adding old_price column: {e}")
        
        try:
            cursor.execute("ALTER TABLE api_product ADD COLUMN stock_quantity INTEGER DEFAULT 0")
            print("Added stock_quantity column to api_product table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("stock_quantity column already exists in api_product table")
            else:
                print(f"Error adding stock_quantity column: {e}")
        
        try:
            cursor.execute("ALTER TABLE api_product ADD COLUMN sku TEXT")
            print("Added sku column to api_product table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("sku column already exists in api_product table")
            else:
                print(f"Error adding sku column: {e}")
        
        try:
            cursor.execute("ALTER TABLE api_product ADD COLUMN weight DECIMAL")
            print("Added weight column to api_product table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("weight column already exists in api_product table")
            else:
                print(f"Error adding weight column: {e}")
        
        try:
            cursor.execute("ALTER TABLE api_product ADD COLUMN dimensions TEXT")
            print("Added dimensions column to api_product table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("dimensions column already exists in api_product table")
            else:
                print(f"Error adding dimensions column: {e}")
        
        try:
            cursor.execute("ALTER TABLE api_product ADD COLUMN is_featured INTEGER DEFAULT 0")
            print("Added is_featured column to api_product table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("is_featured column already exists in api_product table")
            else:
                print(f"Error adding is_featured column: {e}")
        
        # Commit changes
        conn.commit()
        conn.close()
        print("Backend database update completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error updating backend database: {e}")
        return False

def create_admin_user(db_path):
    """Create an admin user if one doesn't exist"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if admin user already exists
        cursor.execute("SELECT id FROM users WHERE email = 'admin@bossshopp.com'")
        admin_user = cursor.fetchone()
        
        if admin_user:
            print("Admin user already exists")
            conn.close()
            return True
        
        # Create admin user
        password = "admin123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO users (name, email, password, is_admin, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, ("Administrator", "admin@bossshopp.com", hashed_password, 1, 1))
        
        conn.commit()
        conn.close()
        print("Admin user created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    # Update frontend database
    frontend_db = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\frontend\database.db"
    update_frontend_database(frontend_db)
    
    # Update backend database
    backend_db = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\backend\db.sqlite3"
    update_backend_database(backend_db)
    
    # Create admin user in frontend database
    create_admin_user(frontend_db)
    
    print("\nDatabase update process completed!")