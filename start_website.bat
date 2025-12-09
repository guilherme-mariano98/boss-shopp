@echo off
TITLE Boss Shopp - Website Starter

echo ========================================
echo BOSS SHOPP - Website Startup Script
echo ========================================

echo Installing/updating Python dependencies...
pip install -r requirements.txt

echo Installing/updating Node.js dependencies...
cd "PI3 (2)/PI3 (1)/PI3/PI2/frontend"
npm install
cd ../../../../..

echo Starting Boss Shopp website...
python start.py

pause