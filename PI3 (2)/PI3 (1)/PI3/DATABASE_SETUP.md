# BOSS SHOPP Database Setup

This document explains how to set up the database for the BOSS SHOPP e-commerce system. You can choose between MySQL or SQLite.

## Prerequisites

### For MySQL:
1. MySQL Server 8.0 or higher
2. Python 3.8 or higher
3. pip (Python package installer)

### For SQLite:
1. Python 3.8 or higher (SQLite is included with Python)

## Database Schema Overview

The BOSS SHOPP database contains 17 tables that support a complete e-commerce workflow:

1. **users** - User accounts and profiles
2. **categories** - Product categories
3. **products** - Product catalog
4. **product_images** - Product images
5. **user_addresses** - User shipping addresses
6. **orders** - Customer orders
7. **order_items** - Items in orders
8. **cart_items** - Shopping cart items
9. **favorites** - User favorite products
10. **product_reviews** - Product reviews and ratings
11. **coupons** - Discount coupons
12. **coupon_usage** - Coupon usage tracking
13. **payment_methods** - User payment methods
14. **payment_transactions** - Payment transaction records
15. **stock_movements** - Inventory tracking
16. **notifications** - User notifications
17. **system_settings** - Application settings

## Setup Methods

### Method 1: SQLite Setup (Recommended for beginners)

SQLite is a lightweight database that requires no installation. It's perfect for development and testing.

1. **Create the database:**
   ```bash
   python create_database_sqlite.py
   ```

2. **Test the connection:**
   ```bash
   python test_database_sqlite.py
   ```

This will create a file named `bossshopp_complete.db` in the current directory.

### Method 2: MySQL Setup

#### Automated Setup (Recommended)

Run the automated setup script:

```bash
# On Windows
setup_bossshopp.bat

# On Linux/Mac
python setup_bossshopp.py
```

This will:
1. Install required Python dependencies
2. Create the database and all tables
3. Insert sample data
4. Test the database connection

#### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create the database:**
   ```bash
   python create_database.py
   ```

3. **Test the connection:**
   ```bash
   python test_database_connection.py
   ```

#### SQL Import

Import the schema directly into MySQL:

```bash
mysql -u root -p < bossshopp_schema.sql
```

## Database Configuration

### For MySQL:
- Host: localhost
- Port: 3306
- User: root
- Password: root
- Database: boss_shopp_complete

To change these settings, modify the configuration in:
- [create_database.py](create_database.py)
- [test_database_connection.py](test_database_connection.py)

### For SQLite:
- Database file: bossshopp_complete.db
- No additional configuration needed

## Sample Data

The database includes:
- 6 product categories
- 24 sample products
- 1 admin user (admin@bossshopp.com / password)
- System settings for the application

## Views

The database includes 3 useful views:
1. **products_with_category** - Products with their category information
2. **orders_with_user** - Orders with user details
3. **sales_statistics** - Daily sales statistics

## Triggers

The database includes 3 triggers for automated operations:
1. **update_product_rating_after_review** - Updates product ratings when reviews are added
2. **generate_order_number** - Automatically generates order numbers
3. **update_stock_after_order** - Updates stock levels when orders are placed

## Troubleshooting

### Connection Issues

If you get connection errors:
1. Verify MySQL server is running
2. Check database credentials in the Python scripts
3. Ensure the MySQL user has proper permissions

### Missing Dependencies

If you get import errors:
```bash
pip install mysql-connector-python
```

### Database Already Exists

If the database already exists, the scripts will update it rather than recreate it.

## Admin Access

After setup, you can access the admin account:
- Email: admin@bossshopp.com
- Password: password

Note: In a production environment, you should change this password immediately.