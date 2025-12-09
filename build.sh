#!/bin/bash
# Build script for Render deployment

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

echo "Build completed successfully!"