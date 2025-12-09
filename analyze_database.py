#!/usr/bin/env python3
"""
Script to analyze the SQLite database structure
"""

import sqlite3
import os

def analyze_database(db_path):
    """Analyze the database structure"""
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return
    
    print(f"Analyzing database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nTables in the database:")
        for table in tables:
            print(f"  - {table[0]}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            
            print(f"    Columns:")
            for column in columns:
                print(f"      {column[1]} ({column[2]}) {'PRIMARY KEY' if column[5] else ''}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"    Row count: {count}")
            
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"Error analyzing database: {e}")

if __name__ == "__main__":
    # Analyze backend database
    backend_db = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\backend\db.sqlite3"
    print("=== BACKEND DATABASE ===")
    analyze_database(backend_db)
    
    # Analyze frontend database if it exists
    frontend_db = r"c:\Users\guilherme54220026\Downloads\PI3 (2) (1)\PI3 (2)\PI3 (1)\PI3\PI2\frontend\database.db"
    if os.path.exists(frontend_db):
        print("\n=== FRONTEND DATABASE ===")
        analyze_database(frontend_db)