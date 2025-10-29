# Security Audit & Password Enforcement App

This project is a web-based application developed for our college curriculum, focusing on web security, user management, and data visualization.

It functions as a complete system for user authentication (registration, login) and features a powerful backend that actively audits user password strength. It includes a comprehensive admin dashboard for monitoring security risks, viewing analytics, and managing user notifications.

## 🚀 Description

The application simulates a corporate portal where users must register and log in. The system's core feature is its automated security audit, which runs checks on user passwords during registration and login to identify vulnerabilities.

The audit module flags passwords that are:

- Too short or lack complexity (e.g., missing uppercase letters, digits, or special characters).
    
- Found in a pre-defined list of common "weak" passwords.
    
- Based on the user's own personal information (name, email, phone, date of birth, etc.).
    

Users with insecure passwords are automatically notified on their dashboard and prompted to change them. The admin panel provides a high-level overview of the organization's security posture, complete with detailed logs, user reports, and interactive analytics.

## ✨ Features

### User Features

- **Secure Registration & Login:** A complete user authentication system.
    
- **Password Hashing:** All user passwords are securely hashed using **bcrypt**.
    
- **Personal Dashboard:** A dedicated dashboard for each user to view their status.
    
- **Vulnerability Notifications:** Users are automatically alerted on their dashboard if their password is weak or compromised.
    
- **Password Reset:** A secure flow for users to reset their password after logging in.
    

### Admin Features

- **Admin-only Login:** A separate, secure login for administrators.
    
- **Interactive Analytics Dashboard:** A rich, single-page application built with JavaScript that visualizes:
    
    - **Password Strength:** A "doughnut" chart showing the ratio of Strong, Weak, and Common passwords.
        
    - **Risk by Department:** A "bar" chart breaking down password vulnerabilities by company department.
        
    - **Login Activity:** A "line" chart tracking successful vs. failed logins over time.
        
- **User Management:** A searchable, sortable table of all registered users, their contact info, and their current password risk status.
    
- **Notify Users:** Admins can send a "Password reset required" notification directly to any user with a weak password with the click of a button.
    
- **Login Audit Logs:** A dedicated page to view and search all successful and failed login attempts with their corresponding timestamp, email, and IP address.
    

## 📸 Screenshots
---

### 👤 User-Facing Pages

**Login Page**
<p align="center">
  <img src="https://raw.githubusercontent.com/navnee1h/security_audit_app/refs/heads/master/screenshots/user_login.png" alt="User Login Screenshot" width="600">
</p>

**User Dashboard with Notification**
<p align="center">
  <img src="https://raw.githubusercontent.com/navnee1h/security_audit_app/refs/heads/master/screenshots/user_dashboard.png" alt="User Dashboard Screenshot" width="600">
</p>

---

### 🧭 Admin Dashboard

**Main Analytics View**
<p align="center">
  <img src="https://raw.githubusercontent.com/navnee1h/security_audit_app/refs/heads/master/screenshots/home_page.png" alt="Admin Home Page" width="600">
</p>

**Analytics Overview**
<p align="center">
  <img src="https://raw.githubusercontent.com/navnee1h/security_audit_app/refs/heads/master/screenshots/analytics.png" alt="Analytics Dashboard" width="600">
</p>

**User Management & Notify Feature**
<p align="center">
  <img src="https://raw.githubusercontent.com/navnee1h/security_audit_app/refs/heads/master/screenshots/users.png" alt="User Management" width="600">
</p>

**Login Audit Logs**
<p align="center">
  <img src="https://raw.githubusercontent.com/navnee1h/security_audit_app/refs/heads/master/screenshots/login_activity.png" alt="Login Activity Logs" width="600">
</p>


---

## 🛠️ Technologies Used

### Backend

- **Python:** Core programming language.
    
- **Flask:** A lightweight web framework for the backend server and REST API.
    
- **bcrypt:** For secure password hashing and verification.
    
- **Pandas:** Used in the API to read, merge, and process data from CSV files for the dashboard.
    

### Frontend

- **HTML5 & CSS3:** For the structure and styling of all web pages.
    
- **Jinja2:** Flask's templating engine for the user-facing pages.
    
- **JavaScript (ES6+):** Powers the entire dynamic admin dashboard.
    
- **Fetch API (AJAX):** Used to asynchronously load all data from the backend API.
    
- **Chart.js & ApexCharts.js:** Used to render all interactive graphs and charts.
    
- **Bootstrap:** The CSS framework used for the admin dashboard's layout and components.
    

### Data Storage

- **CSV Files:** Used as a simple, flat-file database to store user info, security data, notifications, and logs.
    
- **JSON:** Used for application status (`status.json`) and as the format for the API.
    

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
    
    Bash
    
    ```
    git clone https://github.com/navnee1h/Security-audit-app.git
    cd Security-audit-app
    ```
    
2. **Create and activate a virtual environment:**
    
    Bash
    
    ```
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
    
3. **Install the required dependencies:** _(I have created this `requirements.txt` file for you based on your code.)_
    
    Create a file named `requirements.txt` and paste the following into it:
    
    ```
    Flask
    bcrypt
    pandas
    ```
    
    Then, run the installer:
    
    Bash
    
    ```
    pip install -r requirements.txt
    ```
    
4. **Run the application:**
    
    Bash
    
    ```
    python run.py
    ```
    
5. **Access the application:**
    
    - **User Login:** `http://127.0.0.1:5000/login`
        
    - **Admin Login:** `http://127.0.0.1:5000/admin-login`
        
        - **Email:** `admin@gmail.com`
            
        - **Password:** `admin`
            

## 📂 Project Structure

Here is a high-level overview of the project's layout:

```
.
├── admin_dashboard/   # (FRONTEND) All static HTML/CSS/JS files for the admin panel.
│   ├── assets/
│   ├── index.html     # Main dashboard page
│   ├── analytics.html
│   ├── log.html
│   └── users.html
├── app/                 # (BACKEND) The main Flask application source code.
│   ├── routes/          # Flask blueprints that define all app URLs.
│   │   ├── admin.py     # Admin login and notification logic.
│   │   ├── dashboard_routes.py  # The critical API endpoint (/dashboard/api/data).
│   │   └── user.py      # User login, registration, and dashboard logic.
│   ├── templates/       # Jinja2 HTML templates for the user pages.
│   ├── utils/           # Core security logic.
│   │   ├── common_password.py
│   │   ├── personal_info_passwords.py
│   │   └── ...
│   └── __init__.py      # Flask application factory (initializes the app).
├── data/                # (DATA) All data files used by the app.
│   ├── users.csv
│   ├── user_security.csv
│   ├── login-log.txt
│   └── notifications.csv
└── run.py               # (ENTRY POINT) The main script to start the server.
```
### Follow Me On

[Linkedin](https://www.linkedin.com/in/navnee1h/) | [Portfolio](https://navnee1h.github.io/terminal-portfolio)

## 🤝 Usage & Contributions

This project was built for academic purposes. If you find it useful and wish to fork, copy, or build upon this project, I would appreciate it if you could let me know!
