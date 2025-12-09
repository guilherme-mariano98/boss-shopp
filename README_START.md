# Boss Shopp - Website Startup Guide

This guide explains how to start the entire Boss Shopp website using the `start.py` script.

## Prerequisites

Make sure you have Python installed on your system. You'll also need Node.js for the frontend server.

## Installation

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Install the required Node.js packages:
   ```
   cd "PI3 (2)/PI3 (1)/PI3/PI2/frontend"
   npm install
   ```

## Starting the Website

To start the entire website with a single command:

```
python start.py
```

This will:
1. Start the Django backend server on port 8000
2. Start the Node.js frontend server on port 3000

## Accessing the Services

Once started, you can access:
- Main website: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin panel: http://localhost:8000/admin/

## Stopping the Services

To stop all services, press `Ctrl+C` in the terminal where you started the script.

## Alternative: Running as Flask App

You can also run the coordinator as a Flask application:

```
python start.py flask
```

This will start a Flask server on port 5000 with health check endpoints:
- Health check: http://localhost:5000/health