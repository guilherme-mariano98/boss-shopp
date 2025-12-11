@echo off
echo BOSS SHOPP Admin and Vendor Database Test
echo =======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher
    pause
    exit /b 1
)

REM Check if database file exists
if not exist "bossshopp_admin_vendor.db" (
    echo Error: Database file not found!
    echo Please run setup_admin_vendor_db.bat first!
    pause
    exit /b 1
)

REM Run the test script
echo Running database tests...
python test_admin_vendor_db.py

if %errorlevel% equ 0 (
    echo.
    echo Database tests completed successfully!
) else (
    echo.
    echo Database tests failed!
)

pause