from flask import Blueprint, render_template, request, redirect, url_for, session
from app.utils.password_analysis import analyze_personal_passwords
import csv, os, bcrypt
from datetime import datetime
import threading

user_bp = Blueprint('user', __name__)
USER_CSV = 'data/users.csv'
SECURITY_CSV = 'data/user_security.csv'
LOG_FILE = 'data/login-log.txt'

# Ensure necessary files exist
for csv_file, headers in [
    (USER_CSV, ['fullname', 'email', 'phone','department', 'dob', 'gender', 'address']),
    (SECURITY_CSV, ['email', 'password', 'length_ok', 'has_upper', 'has_lower', 'has_digit', 'has_special', 'security_warning'])
]:
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

# ---------------------- PASSWORD ANALYSIS FUNCTION ----------------------
def get_password_flags(password):
    length_ok = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()-_=+[{]}\|;:\'",<.>/?`~' for c in password)
    security_warning = not all([length_ok, has_upper, has_lower, has_digit, has_special])
    return length_ok, has_upper, has_lower, has_digit, has_special, security_warning

# ---------------------- REGISTER ----------------------
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        data = {
            'fullname': request.form['fullname'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'department': request.form['department'],
            'dob': request.form['dob'],
            'gender': request.form['gender'],
            'address': request.form['address'],
            'password': request.form['password']
        }

        # Hash password
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Analyze password strength
        length_ok, has_upper, has_lower, has_digit, has_special, security_warning = get_password_flags(data['password'])

        # Save user info
        with open(USER_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['fullname'], data['email'], data['phone'], data['department'],
                data['dob'], data['gender'], data['address']
            ])

        # Save security info
        with open(SECURITY_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['email'], hashed_pw,
                str(length_ok).lower(), str(has_upper).lower(), str(has_lower).lower(),
                str(has_digit).lower(), str(has_special).lower(),
                str(security_warning).lower()
            ])

        # Run password analysis in background
        def background_analysis():
            users_csv = 'data/users.csv'
            security_csv = 'data/user_security.csv'
            output_csv = 'data/user_security.csv'
            rules_txt = 'app/utils/patterns/rules.txt'
            analyze_personal_passwords(users_csv, security_csv, rules_txt, output_csv)
            print("[DEBUG] Password analysis updated after registration.")

        threading.Thread(target=background_analysis).start()

        return redirect(url_for('user.login'))

    return render_template('register.html', message=message)


# ---------------------- LOGIN ----------------------
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password'].encode('utf-8')

        authenticated = False
        login_status = 'FAILED'
        ip_address = request.remote_addr
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(SECURITY_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    stored_hash = row['password'].encode('utf-8')
                    if bcrypt.checkpw(password_input, stored_hash):
                        authenticated = True
                        login_status = 'SUCCESS'
                    break

        # Log attempt
        with open(LOG_FILE, 'a') as log:
            log.write(f"[{login_time}] {login_status} LOGIN: {email} from IP: {ip_address}\n")

        if authenticated:
            with open(USER_CSV, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['email'] == email:
                        session['user'] = row['fullname']
                        session['email'] = email
                        return render_template('user_dashboard.html', name=row['fullname'])

            # Fallback
            session['user'] = email
            session['email'] = email
            return render_template('user_dashboard.html', name=email)
        else:
            message = "Invalid email or password."

    return render_template('login.html', message=message)

# ---------------------- RESET PASSWORD ----------------------
@user_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'user' not in session or 'email' not in session:
        return redirect(url_for('user.login'))

    message = ''
    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password'].encode('utf-8')
        new_password_raw = request.form['new_password']

        rows = []
        updated = False

        # Analyze new password strength
        length_ok, has_upper, has_lower, has_digit, has_special, security_warning = get_password_flags(new_password_raw)

        with open(SECURITY_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    if bcrypt.checkpw(old_password, row['password'].encode('utf-8')):
                        hashed = bcrypt.hashpw(new_password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        row['password'] = hashed
                        row['length_ok'] = str(length_ok).lower()
                        row['has_upper'] = str(has_upper).lower()
                        row['has_lower'] = str(has_lower).lower()
                        row['has_digit'] = str(has_digit).lower()
                        row['has_special'] = str(has_special).lower()
                        row['security_warning'] = str(security_warning).lower()
                        updated = True
                    else:
                        message = "❌ Old password is incorrect."
                        return render_template('reset_password.html', message=message)
                rows.append(row)

        if updated:
            with open(SECURITY_CSV, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            message = "✅ Password updated successfully."

            # Start password analysis in background
            def background_analysis():
                users_csv = 'data/users.csv'
                security_csv = 'data/user_security.csv'
                output_csv = 'data/user_security.csv'
                rules_txt = 'app/utils/patterns/rules.txt'
                analyze_personal_passwords(users_csv, security_csv, rules_txt, output_csv)
                print("[DEBUG] Password analysis updated after reset.")

            threading.Thread(target=background_analysis).start()

        else:
            message = "❌ User not found or update failed."

    return render_template('reset_password.html', message=message)


# ---------------------- LOGOUT ----------------------
@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('user.login'))
