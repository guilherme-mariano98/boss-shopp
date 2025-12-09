@echo off
echo ========================================
echo BOSS SHOPP DATABASE SETUP
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b %errorlevel%
)

echo.
echo Creating database...
python create_database.py
if %errorlevel% neq 0 (
    echo Error: Failed to create database
    pause
    exit /b %errorlevel%
)

echo.
echo Testing database connection...
python test_database_connection.py
if %errorlevel% neq 0 (
    echo Error: Database connection test failed
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Next steps:
echo 1. Run the backend: cd PI2 ^& python run_backend.py
echo 2. Run the frontend: cd PI2 ^& python serve_frontend.py
echo.
pause