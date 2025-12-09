#!/usr/bin/env python3
"""
BOSS SHOPP Complete Setup Script
Installs dependencies and sets up the database
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_database():
    """Create the database using the create_database.py script"""
    print("Creating database...")
    try:
        subprocess.check_call([sys.executable, "create_database.py"])
        print("✅ Database created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create database: {e}")
        return False

def test_database():
    """Test the database connection"""
    print("Testing database connection...")
    try:
        subprocess.check_call([sys.executable, "test_database_connection.py"])
        print("✅ Database connection test passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("="*60)
    print("BOSS SHOPP COMPLETE SETUP")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Please run this script from the directory containing requirements.txt")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        return
    
    # Create database
    if not create_database():
        print("❌ Setup failed during database creation")
        return
    
    # Test database
    if not test_database():
        print("❌ Setup failed during database testing")
        return
    
    print("\n" + "="*60)
    print("🎉 BOSS SHOPP SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("Next steps:")
    print("1. Run the backend server: python run_backend.py")
    print("2. Run the frontend server: python serve_frontend.py")
    print("3. Access the application at http://localhost:8000")
    print("4. Admin panel: http://localhost:8000/admin")
    print("   Credentials: admin@bossshopp.com / password")
    print("="*60)

if __name__ == "__main__":
    main()