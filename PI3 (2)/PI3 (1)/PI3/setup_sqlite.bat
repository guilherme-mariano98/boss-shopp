@echo off
echo ========================================
echo BOSS SHOPP SQLITE DATABASE SETUP
echo ========================================
echo.

echo Creating SQLite database...
python create_database_sqlite.py
if %errorlevel% neq 0 (
    echo Error: Failed to create database
    pause
    exit /b %errorlevel%
)

echo.
echo Testing database connection...
python test_database_sqlite.py
if %errorlevel% neq 0 (
    echo Error: Database connection test failed
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo SQLITE SETUP COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Database file: bossshopp_complete.db
echo.
echo Next steps:
echo 1. Run the backend: cd PI2 ^& python run_backend.py
echo 2. Run the frontend: cd PI2 ^& python serve_frontend.py
echo.
pause