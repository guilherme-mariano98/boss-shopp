#!/usr/bin/env python3
"""
Flask application to start the entire Boss Shopp website.
This script coordinates the startup of both the frontend (Node.js) and backend (Django) services.
"""

import os
import sys
import subprocess
import threading
import time
import signal
import psutil
import webbrowser
from flask import Flask, jsonify

# Create Flask app
app = Flask(__name__)

# Global variables to track processes
frontend_process = None
backend_process = None
running = True

def kill_process_tree(pid):
    """Kill a process and all its child processes"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        parent.kill()
    except psutil.NoSuchProcess:
        pass

def start_frontend():
    """Start the Node.js frontend server"""
    global frontend_process
    
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'frontend')
    
    try:
        print("Starting frontend server...")
        frontend_process = subprocess.Popen(
            ['node', 'server.js'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Frontend server started with PID {frontend_process.pid}")
        
        # Monitor frontend output
        def monitor_frontend():
            if frontend_process.stdout:
                for line in iter(frontend_process.stdout.readline, b''):
                    print(f"[FRONTEND] {line.decode('utf-8').strip()}")
        
        threading.Thread(target=monitor_frontend, daemon=True).start()
        
    except Exception as e:
        print(f"Error starting frontend: {e}")

def start_backend():
    """Start the Django backend server"""
    global backend_process
    
    backend_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'backend')
    
    try:
        print("Starting backend server...")
        backend_process = subprocess.Popen(
            [sys.executable, 'run_server.py'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Backend server started with PID {backend_process.pid}")
        
        # Monitor backend output
        def monitor_backend():
            if backend_process.stdout:
                for line in iter(backend_process.stdout.readline, b''):
                    print(f"[BACKEND] {line.decode('utf-8').strip()}")
        
        threading.Thread(target=monitor_backend, daemon=True).start()
        
    except Exception as e:
        print(f"Error starting backend: {e}")

def open_website():
    """Open the website in the default browser"""
    time.sleep(8)  # Wait for servers to start
    try:
        webbrowser.open("http://localhost:3000")
        print("Website opened in your default browser!")
        print("The website is now optimized for mobile devices!")
    except Exception as e:
        print(f"Could not open browser: {e}")

def stop_servers():
    """Stop all running servers"""
    global frontend_process, backend_process, running
    
    print("\nShutting down servers...")
    running = False
    
    if frontend_process and frontend_process.poll() is None:
        print("Stopping frontend server...")
        kill_process_tree(frontend_process.pid)
        frontend_process.wait()
    
    if backend_process and backend_process.poll() is None:
        print("Stopping backend server...")
        kill_process_tree(backend_process.pid)
        backend_process.wait()
    
    print("All servers stopped.")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\nReceived interrupt signal')
    stop_servers()
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "OK",
        "message": "Boss Shopp main coordinator is running",
        "services": {
            "frontend": "http://localhost:3000",
            "backend_api": "http://localhost:8000/api/",
            "backend_admin": "http://localhost:8000/admin/"
        },
        "mobile_support": "Enabled - Website optimized for mobile devices"
    })

@app.route('/health')
def health():
    """Detailed health check endpoint"""
    frontend_status = "running" if frontend_process and frontend_process.poll() is None else "stopped"
    backend_status = "running" if backend_process and backend_process.poll() is None else "stopped"
    
    return jsonify({
        "status": "OK",
        "frontend": {
            "status": frontend_status,
            "pid": frontend_process.pid if frontend_process else None
        },
        "backend": {
            "status": backend_status,
            "pid": backend_process.pid if backend_process else None
        },
        "mobile_support": "enabled"
    })

def main():
    """Main function to start all services"""
    print("=" * 50)
    print("BOSS SHOPP - Website Coordinator")
    print("=" * 50)
    print("Mobile support: ENABLED")
    print("Optimizations for touch devices and small screens")
    
    # Start services
    start_backend()
    time.sleep(5)  # Give backend time to initialize
    start_frontend()
    
    # Open website in browser
    browser_thread = threading.Thread(target=open_website, daemon=True)
    browser_thread.start()
    
    # Wait a moment for services to start
    time.sleep(3)
    
    print("\nServices started:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:8000/api/")
    print("- Backend Admin: http://localhost:8000/admin/")
    print("\nThe website should now be open in your browser!")
    print("Mobile optimizations are enabled for all devices!")
    print("If not, please manually visit: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services")
    
    # Keep the main thread alive
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_servers()

if __name__ == "__main__":
    # If command line arguments are provided, run as Flask app
    if len(sys.argv) > 1 and sys.argv[1] == "flask":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        # Otherwise run the coordinator
        main()