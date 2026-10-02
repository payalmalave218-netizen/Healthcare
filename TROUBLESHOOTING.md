# Troubleshooting Guide

## Quick Fixes

### 1. Run the Diagnostic Script First
```bash
python test_setup.py
```
This will check all requirements and tell you what's wrong.

### 2. Use the Debug Script (Windows)
Double-click `run_debug.bat` - it will diagnose and run the application.

---

## Common Errors and Solutions

### Error: "Python is not recognized"
**Problem**: Python is not installed or not in PATH

**Solution**:
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

---

### Error: "No module named 'flask'"
**Problem**: Flask is not installed

**Solution**:
```bash
pip install Flask
# or
python -m pip install Flask
# or
pip install -r requirements.txt
```

---

### Error: "Port 5000 already in use"
**Problem**: Another application is using port 5000

**Solutions**:
1. **Find and close the application using port 5000:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   
   # Mac/Linux
   lsof -ti:5000 | xargs kill
   ```

2. **Or change the port in app.py:**
   - Open `app.py`
   - Find line: `app.run(debug=True, host='127.0.0.1', port=5000)`
   - Change `5000` to `5001` or another port
   - Update URL to: `http://localhost:5001`

---

### Error: "FileNotFoundError: database/schema.sql"
**Problem**: File path issue or wrong working directory

**Solutions**:
1. Make sure you're running from the project root directory
2. Check that `database/schema.sql` exists
3. Run: `python test_setup.py` to verify file structure

---

### Error: "sqlite3.OperationalError: no such table"
**Problem**: Database not initialized properly

**Solutions**:
1. Delete `hospital.db` file if it exists
2. Run the application again - it will recreate the database
3. Or manually initialize:
   ```python
   python -c "from app import init_db; init_db()"
   ```

---

### Error: "TemplateNotFound"
**Problem**: Templates folder not found

**Solutions**:
1. Verify `templates/` folder exists
2. Make sure you're running from the project root
3. Check that all HTML files are in `templates/` folder

---

### Error: "Permission denied" or "Access denied"
**Problem**: File permissions issue

**Solutions**:
1. Run terminal/command prompt as Administrator
2. Check file/folder permissions
3. Make sure you have write access to the directory

---

### Error: "Connection refused" in browser
**Problem**: Server not running or wrong URL

**Solutions**:
1. Make sure the server is running (check terminal for "Running on...")
2. Use correct URL: `http://localhost:5000` or `http://127.0.0.1:5000`
3. Don't use `https://` - use `http://`
4. Check firewall settings

---

### Error: "Cannot login with admin/admin123"
**Problem**: Database not initialized or password hash issue

**Solutions**:
1. Delete `hospital.db` file
2. Restart the application
3. Try login again
4. Check terminal for initialization messages

---

### Error: "ModuleNotFoundError: No module named 'secrets'"
**Problem**: Using Python 2.x instead of Python 3.x

**Solutions**:
1. Install Python 3.7 or higher
2. Use `python3` instead of `python`:
   ```bash
   python3 app.py
   ```

---

## Step-by-Step Debugging

### Step 1: Verify Python Installation
```bash
python --version
# Should show Python 3.7 or higher
```

### Step 2: Verify Flask Installation
```bash
python -c "import flask; print(flask.__version__)"
# Should show Flask version number
```

### Step 3: Check File Structure
Run the diagnostic script:
```bash
python test_setup.py
```

### Step 4: Check Port Availability
```bash
# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000
```

### Step 5: Run with Verbose Output
```bash
python app.py
```
Look for error messages in the terminal output.

---

## Still Not Working?

1. **Check the terminal/command prompt output** - it usually shows the exact error
2. **Run the diagnostic script**: `python test_setup.py`
3. **Check Python version**: Must be 3.7 or higher
4. **Verify all files exist**: Use `test_setup.py` to check
5. **Try a fresh start**:
   - Delete `hospital.db`
   - Delete `__pycache__` folder if it exists
   - Run `python app.py` again

---

## Getting Help

When asking for help, provide:
1. Error message from terminal
2. Output of `python test_setup.py`
3. Python version: `python --version`
4. Operating system (Windows/Mac/Linux)
5. What you tried so far
