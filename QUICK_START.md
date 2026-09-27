# Quick Start Guide

## How to Run HEALIX HOSPITAL

### Method 1: Using the Batch File (Windows - Easiest)

1. **Double-click `run.bat`**
   - This will automatically install dependencies and start the server

2. **Open your browser** and go to: `http://localhost:5000`

3. **Login with:**
   - Username: `admin`
   - Password: `admin123`

---

### Method 2: Manual Steps

#### Step 1: Open Terminal/Command Prompt

- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux**: Open Terminal

#### Step 2: Navigate to Project Folder

```bash
cd "C:\Users\ASUS\OneDrive\Desktop\Hospital Management system.py"
```

#### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If `pip` doesn't work, try:
- `python -m pip install -r requirements.txt`
- `pip3 install -r requirements.txt`

#### Step 4: Run the Application

```bash
python app.py
```

**Note**: If `python` doesn't work, try:
- `python3 app.py`
- `py app.py`

#### Step 5: Access the Application

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://localhost:5000**
3. You should see the login page

#### Step 6: Login

- **Username**: `admin`
- **Password**: `admin123`

---

## Troubleshooting

### Problem: "Python is not recognized"

**Solution**: 
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal/command prompt after installation

### Problem: "pip is not recognized"

**Solution**:
- Try `python -m pip install -r requirements.txt`
- Or install pip separately

### Problem: "Port 5000 already in use"

**Solution**:
- Close any other applications using port 5000
- Or modify `app.py` line 260 to use a different port:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
  ```

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution**:
- Make sure you ran: `pip install -r requirements.txt`
- Try: `pip install Flask Werkzeug`

### Problem: Database errors

**Solution**:
- Delete `hospital.db` file if it exists
- The database will be created automatically on first run

---

## What Happens When You Run?

1. ✅ Flask server starts on port 5000
2. ✅ Database (`hospital.db`) is created automatically
3. ✅ Default admin user is created
4. ✅ You can access the web interface at http://localhost:5000

---

## Stopping the Server

- Press `Ctrl + C` in the terminal/command prompt
- Or close the terminal window

---

## Need Help?

- Check the `README.md` file for more details
- Make sure all files are in the correct folders
- Verify Python version (3.7 or higher recommended)
