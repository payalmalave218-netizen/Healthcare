#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnostic script to check if everything is set up correctly
"""
import sys
import os
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("="*60)
print("HEALIX HOSPITAL - Setup Diagnostic")
print("="*60)
print()

# Check Python version
print("1. Checking Python version...")
print(f"   Python version: {sys.version}")
if sys.version_info < (3, 7):
    print("   [WARNING] Python 3.7 or higher recommended")
else:
    print("   [OK] Python version OK")
print()

# Check Flask installation
print("2. Checking Flask installation...")
try:
    import flask
    print(f"   [OK] Flask {flask.__version__} is installed")
except ImportError:
    print("   [ERROR] Flask is NOT installed")
    print("   Run: pip install Flask")
    sys.exit(1)
print()

# Check file structure
print("3. Checking file structure...")
files_to_check = [
    'app.py',
    'database/schema.sql',
    'templates/base.html',
    'templates/login.html',
    'static/css/style.css',
    'static/js/main.js'
]

all_files_exist = True
for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"   [OK] {file_path}")
    else:
        print(f"   [ERROR] {file_path} - MISSING!")
        all_files_exist = False

if not all_files_exist:
    print("\n   [WARNING] Some files are missing. Please check the project structure.")
    sys.exit(1)
print()

# Check database directory
print("4. Checking database directory...")
if os.path.exists('database'):
    print("   [OK] database/ directory exists")
else:
    print("   [ERROR] database/ directory missing!")
    sys.exit(1)
print()

# Check if database exists
print("5. Checking database file...")
if os.path.exists('hospital.db'):
    print("   [OK] hospital.db exists")
    try:
        import sqlite3
        conn = sqlite3.connect('hospital.db')
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"   [OK] Database has {len(tables)} tables")
        conn.close()
    except Exception as e:
        print(f"   [WARNING] Database exists but may be corrupted: {e}")
else:
    print("   [INFO] hospital.db will be created on first run")
print()

# Test database initialization
print("6. Testing database initialization...")
try:
    schema_path = os.path.join('database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        print("   [OK] schema.sql can be read")
    else:
        print("   [ERROR] schema.sql not found!")
        sys.exit(1)
except Exception as e:
    print(f"   [ERROR] Error reading schema.sql: {e}")
    sys.exit(1)
print()

# Check port availability
print("7. Checking port 5000...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    if result == 0:
        print("   [WARNING] Port 5000 is already in use!")
        print("   You may need to stop another application or change the port.")
    else:
        print("   [OK] Port 5000 is available")
except Exception as e:
    print(f"   [WARNING] Could not check port: {e}")
print()

print("="*60)
print("Diagnostic complete!")
print("="*60)
print()
print("If all checks passed, you can run the application with:")
print("  python app.py")
print()
print("Then open your browser to: http://localhost:5000")
print("Login: admin / admin123")
print()
