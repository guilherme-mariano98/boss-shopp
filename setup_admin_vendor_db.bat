@echo off
echo BOSS SHOPP Admin and Vendor Database Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking for required packages...
python -c "import bcrypt" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing bcrypt package...
    pip install bcrypt
    if %errorlevel% neq 0 (
        echo Error: Failed to install bcrypt package
        pause
        exit /b 1
    )
)

REM Run the setup script
echo.
echo Setting up database...
python setup_admin_vendor_db.py

if %errorlevel% equ 0 (
    echo.
    echo Database setup completed successfully!
    echo.
    echo To test the database, run: test_admin_vendor_db.bat
) else (
    echo.
    echo Database setup failed!
)

pause