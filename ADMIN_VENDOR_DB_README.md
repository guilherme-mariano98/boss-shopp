# BOSS SHOPP Admin and Vendor Database

This directory contains the SQLite database schema and setup scripts for the BOSS SHOPP e-commerce platform with support for admin and vendor roles.

## Features

1. **Admin Role**:
   - Full access to all system features
   - User management
   - Product management
   - Order management
   - System configuration

2. **Vendor Role**:
   - Manage their own products
   - View their sales statistics
   - Track commissions
   - Manage inventory for their products

3. **User Management**:
   - Users can be admins, vendors, or regular customers
   - Vendor application workflow
   - Role-based access control

## Files Included

- `admin_vendor_sqlite_schema.sql` - Complete SQLite database schema
- `setup_admin_vendor_db.py` - Python script to initialize the database
- `test_admin_vendor_db.py` - Python script to test the database
- `setup_admin_vendor_db.bat` - Windows batch file to run setup
- `test_admin_vendor_db.bat` - Windows batch file to run tests

## Database Schema Highlights

### Users Table Enhancements
- `is_admin` BOOLEAN - Flag for administrator users
- `is_vendor` BOOLEAN - Flag for vendor users
- `vendor_id` in products table - Links products to their vendors

### New Tables
- `vendor_applications` - For users requesting vendor status
- `vendor_commissions` - Tracks commissions for vendor sales

### Views
- `vendor_products` - Products with vendor information
- `vendor_statistics` - Sales statistics by vendor

## Default Users

After setup, the database will contain:

1. **Administrator**:
   - Email: `admin@bossshopp.com`
   - Password: `admin123`

2. **Vendor**:
   - Email: `vendor@bossshopp.com`
   - Password: `vendor123`

## Setup Instructions

### Windows
1. Double-click `setup_admin_vendor_db.bat`
2. Wait for the setup to complete
3. To test, double-click `test_admin_vendor_db.bat`

### Manual Setup
```bash
# Install required packages
pip install bcrypt

# Run setup script
python setup_admin_vendor_db.py

# Run test script
python test_admin_vendor_db.py
```

## Database Structure

The database includes all standard e-commerce tables plus enhancements for admin and vendor roles:

- Users and authentication
- Products and categories
- Shopping cart and orders
- Reviews and ratings
- Coupons and discounts
- Payment processing
- Inventory management
- Notifications
- System settings

## Vendor Features

Vendors can:
- Add/update/delete their own products
- View sales reports for their products
- Track commission earnings
- Manage inventory levels
- Respond to customer reviews

Admins can:
- Approve/reject vendor applications
- Monitor all vendor activity
- Configure commission rates
- View overall vendor performance

## Security Notes

- Passwords are hashed using bcrypt
- Role-based access control is enforced at the application level
- Vendor applications require admin approval
- All financial transactions are tracked

## Testing

The test script verifies:
- Database connectivity
- Table creation
- Default user creation
- Role assignments
- View functionality

Run `test_admin_vendor_db.py` to verify everything is working correctly.