import urllib.request
import urllib.error
from flask import Flask
from flask_cors import CORS
import threading
import time
import sys
import os

# Add project root to path to import app
sys.path.append(os.getcwd())

try:
    from app import create_app
except ImportError:
    print("Could not import app. Make sure you are in the project root.")
    sys.exit(1)

def run_server(app):
    # Suppress flask banner
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(port=5001, use_reloader=False)

def verify_cors():
    # Start server in a thread
    app = create_app()
    server_thread = threading.Thread(target=run_server, args=(app,))
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    base_url = "http://localhost:5001"
    
    print("--- Verifying CORS ---")
    
    # Test OPTIONS request (Preflight)
    print("\nTesting OPTIONS request...")
    try:
        req = urllib.request.Request(f"{base_url}/estudiantes/", method="OPTIONS")
        req.add_header("Origin", "http://localhost:3000")
        req.add_header("Access-Control-Request-Method", "GET")
        req.add_header("Access-Control-Request-Headers", "Content-Type")
        
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.status}")
            print("Headers:")
            headers = response.info()
            for k, v in headers.items():
                if "Access-Control" in k:
                    print(f"  {k}: {v}")
            
            if response.status == 200 and "Access-Control-Allow-Origin" in headers:
                print("OPTIONS request successful")
            else:
                print("OPTIONS request failed")
            
    except urllib.error.HTTPError as e:
        print(f"Error testing OPTIONS: {e}")
    except Exception as e:
        print(f"Error testing OPTIONS: {e}")

    # Test GET request
    print("\nTesting GET request...")
    try:
        req = urllib.request.Request(f"{base_url}/estudiantes/", method="GET")
        req.add_header("Origin", "http://localhost:3000")
        
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.status}")
            print("Headers:")
            headers = response.info()
            for k, v in headers.items():
                if "Access-Control" in k:
                    print(f"  {k}: {v}")
                
            if "Access-Control-Allow-Origin" in headers:
                print("GET request has CORS headers")
            else:
                print("GET request missing CORS headers")

    except urllib.error.HTTPError as e:
        print(f"Error testing GET: {e}")
    except Exception as e:
        print(f"Error testing GET: {e}")

if __name__ == "__main__":
    verify_cors()
