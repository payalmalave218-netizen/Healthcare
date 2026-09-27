from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

DATABASE = 'hospital.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        if not os.path.exists(schema_path):
            # Try relative path
            schema_path = 'database/schema.sql'
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        conn = get_db()
        # Execute the entire schema
        conn.executescript(schema)
        conn.commit()
        conn.close()
        print("[OK] Database initialized successfully!")
    except sqlite3.IntegrityError as e:
        # User already exists, that's okay
        print("[INFO] Database already initialized (admin user exists)")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        raise

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, hash_password(password))
        ).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    total_patients = conn.execute('SELECT COUNT(*) as count FROM patients').fetchone()['count']
    total_appointments = conn.execute('SELECT COUNT(*) as count FROM appointments').fetchone()['count']
    recent_patients = conn.execute(
        'SELECT * FROM patients ORDER BY created_at DESC LIMIT 5'
    ).fetchall()
    conn.close()
    
    return render_template('dashboard.html', 
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         recent_patients=recent_patients)

@app.route('/patients')
def patients():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    search = request.args.get('search', '')
    if search:
        patients = conn.execute(
            'SELECT * FROM patients WHERE first_name LIKE ? OR last_name LIKE ? OR patient_id LIKE ?',
            (f'%{search}%', f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        patients = conn.execute('SELECT * FROM patients ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('patients.html', patients=patients, search=search)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        conn = get_db()
        # Generate unique patient ID
        patient_id = f"PAT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        conn.execute('''
            INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, gender,
                                 phone, email, address, blood_group, emergency_contact_name,
                                 emergency_contact_phone, medical_history)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient_id,
            request.form['first_name'],
            request.form['last_name'],
            request.form['date_of_birth'],
            request.form['gender'],
            request.form.get('phone', ''),
            request.form.get('email', ''),
            request.form.get('address', ''),
            request.form.get('blood_group', ''),
            request.form.get('emergency_contact_name', ''),
            request.form.get('emergency_contact_phone', ''),
            request.form.get('medical_history', '')
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('patients'))
    
    return render_template('add_patient.html')

@app.route('/patients/<int:patient_id>')
def view_patient(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
    appointments = conn.execute(
        'SELECT * FROM appointments WHERE patient_id = ? ORDER BY appointment_date DESC',
        (patient_id,)
    ).fetchall()
    medical_records = conn.execute(
        'SELECT * FROM medical_records WHERE patient_id = ? ORDER BY record_date DESC',
        (patient_id,)
    ).fetchall()
    conn.close()
    
    if not patient:
        return redirect(url_for('patients'))
    
    return render_template('view_patient.html', 
                         patient=patient,
                         appointments=appointments,
                         medical_records=medical_records)

@app.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
    
    if not patient:
        conn.close()
        return redirect(url_for('patients'))
    
    if request.method == 'POST':
        conn.execute('''
            UPDATE patients SET first_name = ?, last_name = ?, date_of_birth = ?, gender = ?,
                              phone = ?, email = ?, address = ?, blood_group = ?,
                              emergency_contact_name = ?, emergency_contact_phone = ?,
                              medical_history = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            request.form['first_name'],
            request.form['last_name'],
            request.form['date_of_birth'],
            request.form['gender'],
            request.form.get('phone', ''),
            request.form.get('email', ''),
            request.form.get('address', ''),
            request.form.get('blood_group', ''),
            request.form.get('emergency_contact_name', ''),
            request.form.get('emergency_contact_phone', ''),
            request.form.get('medical_history', ''),
            patient_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('view_patient', patient_id=patient_id))
    
    conn.close()
    return render_template('edit_patient.html', patient=patient)

@app.route('/patients/<int:patient_id>/delete', methods=['POST'])
def delete_patient(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    conn.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('patients'))

@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    appointments = conn.execute('''
        SELECT a.*, p.first_name, p.last_name, p.patient_id as pat_id
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    ''').fetchall()
    conn.close()
    
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    if request.method == 'POST':
        conn.execute('''
            INSERT INTO appointments (patient_id, appointment_date, appointment_time,
                                     doctor_name, department, reason, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['patient_id'],
            request.form['appointment_date'],
            request.form['appointment_time'],
            request.form.get('doctor_name', ''),
            request.form.get('department', ''),
            request.form.get('reason', ''),
            request.form.get('status', 'scheduled'),
            request.form.get('notes', '')
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('appointments'))
    
    patients = conn.execute('SELECT id, patient_id, first_name, last_name FROM patients ORDER BY first_name').fetchall()
    conn.close()
    return render_template('add_appointment.html', patients=patients)

if __name__ == '__main__':
    try:
        # Initialize database if it doesn't exist
        if not os.path.exists(DATABASE):
            print("Initializing database...")
            init_db()
        else:
            # Check if tables exist, if not initialize
            conn = get_db()
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone() is None:
                print("Database exists but tables missing. Initializing...")
                conn.close()
                init_db()
            else:
                conn.close()
        
        print("\n" + "="*50)
        print("HEALIX HOSPITAL")
        print("="*50)
        print(f"Server running at: http://localhost:5000")
        print(f"Login: admin / admin123")
        print("="*50 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"\nERROR: Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Flask is installed: pip install Flask")
        print("2. Check if port 5000 is available")
        print("3. Verify all files are in the correct folders")
        import traceback
        traceback.print_exc()
