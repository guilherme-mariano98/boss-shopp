#!/bin/bash

echo "========================================"
echo "BOSS SHOPP - Website Startup Script"
echo "========================================"

echo "Installing/updating Python dependencies..."
pip install -r requirements.txt

echo "Installing/updating Node.js dependencies..."
cd src/frontend
npm install
cd ../..

echo "Starting Boss Shopp website..."
python scripts/start.py