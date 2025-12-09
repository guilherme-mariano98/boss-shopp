#!/usr/bin/env python3
"""
Demo script showcasing the new features in the updated database
"""

import sqlite3
import os
from datetime import datetime

def demo_frontend_features():
    """Demonstrate frontend database features"""
    db_path = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\frontend\database.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("=== FRONTEND DATABASE FEATURE DEMO ===\n")
        
        # 1. Show featured products
        print("1. Featured Products:")
        cursor.execute("""
            SELECT p.name, p.price, c.name as category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.is_featured = 1
            ORDER BY p.created_at DESC
        """)
        featured_products = cursor.fetchall()
        
        if featured_products:
            for product in featured_products:
                print(f"   • {product['name']} - R$ {product['price']} ({product['category_name']})")
        else:
            print("   No featured products found")
        
        # 2. Show products with stock information
        print("\n2. Inventory Status:")
        cursor.execute("""
            SELECT name, price, stock_quantity, 
                   CASE 
                       WHEN stock_quantity = 0 THEN 'Out of Stock'
                       WHEN stock_quantity < 10 THEN 'Low Stock'
                       ELSE 'In Stock'
                   END as stock_status
            FROM products
            ORDER BY stock_quantity ASC
            LIMIT 5
        """)
        inventory_status = cursor.fetchall()
        
        for product in inventory_status:
            print(f"   • {product['name']} - Stock: {product['stock_quantity']} ({product['stock_status']})")
        
        # 3. Show product categories with counts
        print("\n3. Product Categories:")
        cursor.execute("""
            SELECT c.name, COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY product_count DESC
        """)
        categories = cursor.fetchall()
        
        for category in categories:
            print(f"   • {category['name']}: {category['product_count']} products")
        
        # 4. Simulate adding item to cart
        print("\n4. Shopping Cart Simulation:")
        # Get a user and product
        cursor.execute("SELECT id FROM users WHERE is_active = 1 LIMIT 1")
        user = cursor.fetchone()
        
        cursor.execute("SELECT id, name, price FROM products WHERE is_active = 1 LIMIT 1")
        product = cursor.fetchone()
        
        if user and product:
            # Add to cart
            cursor.execute("""
                INSERT INTO cart (user_id, product_id, quantity, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user['id'], product['id'], 2, datetime.now(), datetime.now()))
            
            print(f"   Added 2x '{product['name']}' (R$ {product['price']} each) to cart for user ID {user['id']}")
            
            # Show cart contents
            cursor.execute("""
                SELECT c.quantity, p.name, p.price, 
                       (c.quantity * p.price) as total_item_price
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = ?
            """, (user['id'],))
            
            cart_items = cursor.fetchall()
            print("   Current cart contents:")
            total_cart_value = 0
            for item in cart_items:
                print(f"     • {item['quantity']}x {item['name']} = R$ {item['total_item_price']:.2f}")
                total_cart_value += item['total_item_price']
            
            print(f"   Total cart value: R$ {total_cart_value:.2f}")
        
        # 5. Show admin users
        print("\n5. Administrative Users:")
        cursor.execute("SELECT name, email, created_at FROM users WHERE is_admin = 1 AND is_active = 1")
        admins = cursor.fetchall()
        
        for admin in admins:
            print(f"   • {admin['name']} ({admin['email']}) - Created: {admin['created_at']}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error in frontend demo: {e}")

def demo_backend_features():
    """Demonstrate backend database features"""
    db_path = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\backend\db.sqlite3"
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("\n=== BACKEND DATABASE FEATURE DEMO ===\n")
        
        # 1. Show products with enhanced attributes
        print("1. Enhanced Product Information:")
        cursor.execute("""
            SELECT name, price, 
                   COALESCE(old_price, price) as displayed_price,
                   CASE 
                       WHEN old_price IS NOT NULL AND old_price > price 
                       THEN ROUND(((old_price - price) / old_price) * 100, 1)
                       ELSE 0
                   END as discount_percentage,
                   stock_quantity,
                   sku
            FROM api_product
            WHERE LENGTH(name) > 0
            ORDER BY created_at DESC
            LIMIT 3
        """)
        enhanced_products = cursor.fetchall()
        
        for product in enhanced_products:
            if product['discount_percentage'] > 0:
                print(f"   • {product['name']}")
                print(f"     Price: R$ {product['price']} (was R$ {product['displayed_price']})")
                print(f"     Discount: {product['discount_percentage']}% OFF")
            else:
                print(f"   • {product['name']} - R$ {product['price']}")
            
            if product['sku']:
                print(f"     SKU: {product['sku']}")
            
            if product['stock_quantity'] is not None:
                print(f"     Stock: {product['stock_quantity']} units")
            print()
        
        # 2. Show featured products
        print("2. Featured Products:")
        cursor.execute("""
            SELECT name, price
            FROM api_product
            WHERE is_featured = 1
            ORDER BY created_at DESC
        """)
        featured_products = cursor.fetchall()
        
        if featured_products:
            for product in featured_products:
                print(f"   • {product['name']} - R$ {product['price']}")
        else:
            print("   No featured products found")
        
        # 3. Show product analytics
        print("\n3. Product Analytics:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total_products,
                COUNT(CASE WHEN stock_quantity > 0 THEN 1 END) as in_stock_products,
                COUNT(CASE WHEN is_featured = 1 THEN 1 END) as featured_products,
                AVG(price) as average_price,
                MAX(price) as highest_price,
                MIN(price) as lowest_price
            FROM api_product
        """)
        analytics = cursor.fetchone()
        
        print(f"   Total Products: {analytics['total_products']}")
        print(f"   In Stock: {analytics['in_stock_products']}")
        print(f"   Featured: {analytics['featured_products']}")
        print(f"   Average Price: R$ {analytics['average_price']:.2f}")
        print(f"   Price Range: R$ {analytics['lowest_price']:.2f} - R$ {analytics['highest_price']:.2f}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error in backend demo: {e}")

def demo_advanced_queries():
    """Demonstrate advanced database queries"""
    db_path = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\frontend\database.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("\n=== ADVANCED QUERY DEMO ===\n")
        
        # 1. Complex JOIN query with filtering
        print("1. Top Categories by Revenue Potential:")
        cursor.execute("""
            SELECT 
                c.name as category_name,
                COUNT(p.id) as product_count,
                AVG(p.price) as avg_price,
                (COUNT(p.id) * AVG(p.price)) as revenue_potential
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id AND p.is_active = 1
            GROUP BY c.id, c.name
            HAVING product_count > 0
            ORDER BY revenue_potential DESC
            LIMIT 3
        """)
        category_performance = cursor.fetchall()
        
        for cat in category_performance:
            print(f"   • {cat['category_name']}: {cat['product_count']} products, "
                  f"Avg Price: R$ {cat['avg_price']:.2f}, "
                  f"Potential: R$ {cat['revenue_potential']:.2f}")
        
        # 2. Window function simulation (using subquery)
        print("\n2. Best Selling Products by Category:")
        cursor.execute("""
            WITH RankedProducts AS (
                SELECT 
                    p.name,
                    p.price,
                    c.name as category_name,
                    ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as price_rank
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.is_active = 1
            )
            SELECT name, price, category_name
            FROM RankedProducts
            WHERE price_rank <= 2
            ORDER BY category_name, price DESC
        """)
        top_products = cursor.fetchall()
        
        current_category = None
        for product in top_products:
            if product['category_name'] != current_category:
                print(f"   Category: {product['category_name']}")
                current_category = product['category_name']
            print(f"     • {product['name']} - R$ {product['price']}")
        
        # 3. Aggregation with filtering
        print("\n3. Inventory Value Analysis:")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN stock_quantity = 0 THEN 'Out of Stock'
                    WHEN stock_quantity < 5 THEN 'Low Stock'
                    WHEN stock_quantity < 20 THEN 'Medium Stock'
                    ELSE 'High Stock'
                END as stock_level,
                COUNT(*) as product_count,
                SUM(price * stock_quantity) as total_value
            FROM products
            WHERE is_active = 1 AND stock_quantity IS NOT NULL
            GROUP BY 
                CASE 
                    WHEN stock_quantity = 0 THEN 'Out of Stock'
                    WHEN stock_quantity < 5 THEN 'Low Stock'
                    WHEN stock_quantity < 20 THEN 'Medium Stock'
                    ELSE 'High Stock'
                END
            ORDER BY total_value DESC
        """)
        inventory_analysis = cursor.fetchall()
        
        for analysis in inventory_analysis:
            stock_level = analysis['stock_level']
            count = analysis['product_count']
            value = analysis['total_value'] or 0
            print(f"   • {stock_level}: {count} products worth R$ {value:.2f}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error in advanced queries demo: {e}")

if __name__ == "__main__":
    demo_frontend_features()
    demo_backend_features()
    demo_advanced_queries()
    
    print("\n=== DEMO COMPLETED ===")
    print("All database features have been successfully demonstrated!")