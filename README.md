# HEALIX HOSPITAL

A modern, web-based hospital management system built with Flask (Python), SQLite, HTML, and CSS. This system provides a comprehensive portal for managing patient data, appointments, and medical records.

## Features

- 🔐 **Secure Login System** - User authentication with session management
- 👥 **Patient Management** - Add, view, edit, and delete patient records
- 📅 **Appointment Scheduling** - Schedule and manage patient appointments
- 📊 **Dashboard** - Overview of key statistics and recent activities
- 🎨 **Modern UI** - Beautiful, responsive design with smooth animations
- 🔍 **Search Functionality** - Quick search for patients by name or ID
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices

## Installation

1. **Clone or download the project**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Open your web browser and navigate to: `http://localhost:5000`
   - Default login credentials:
     - Username: `admin`
     - Password: `admin123`

## Project Structure

```
HEALIX HOSPITAL/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── hospital.db           # SQLite database (created automatically)
│
├── database/
│   └── schema.sql        # Database schema
│
├── templates/
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard page
│   ├── patients.html     # Patient list page
│   ├── add_patient.html  # Add patient form
│   ├── view_patient.html # Patient details page
│   ├── edit_patient.html # Edit patient form
│   ├── appointments.html # Appointments list
│   └── add_appointment.html # Schedule appointment form
│
└── static/
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── main.js       # JavaScript functionality
```

## Database Schema

The system uses SQLite with the following main tables:

- **users** - User authentication and roles
- **patients** - Patient personal and medical information
- **appointments** - Appointment scheduling and management
- **medical_records** - Medical history and records

## Usage

### Login
- Access the login page and enter your credentials
- Default admin account is created automatically

### Dashboard
- View key statistics and recent patients
- Quick access to common actions

### Patient Management
- **Add Patient**: Click "Add New Patient" and fill in the form
- **View Patient**: Click the eye icon to view full patient details
- **Edit Patient**: Click the edit icon to modify patient information
- **Delete Patient**: Click the delete icon (with confirmation)
- **Search**: Use the search bar to find patients quickly

### Appointments
- Schedule new appointments for patients
- View all scheduled appointments
- Track appointment status

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## Security Notes

⚠️ **Important**: This is a development/demo system. For production use:

1. Use a more secure password hashing method (bcrypt, argon2)
2. Implement proper session security
3. Add CSRF protection
4. Use environment variables for sensitive data
5. Implement proper input validation and sanitization
6. Use HTTPS in production
7. Add rate limiting and authentication middleware

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or create an issue in the repository.
