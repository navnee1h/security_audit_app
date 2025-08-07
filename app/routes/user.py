from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.personal_info_passwords import check_for_personal_info
from app.utils.common_password import is_common_password
import csv
import os
import bcrypt
from datetime import datetime

user_bp = Blueprint('user', __name__)
USER_CSV = 'data/users.csv'
SECURITY_CSV = 'data/user_security.csv'
LOG_FILE = 'data/login-log.txt'

# --- CONFIGURATION ---
# [NEW] This is the new boolean variable.
# Set to False to allow passwords with personal info (but still flag them).
# Set to True to block users from creating passwords with personal info.
ENFORCE_PERSONAL_INFO_CHECK = False

# Ensure necessary files exist
for csv_file, headers in [
    (USER_CSV, ['fullname', 'email', 'phone','department', 'dob', 'gender', 'address']),
    (SECURITY_CSV, ['email', 'password', 'length_ok', 'has_upper', 'has_lower', 'has_digit', 'has_special', 'common_password', 'used_personal_info'])
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
    has_special = any(c in '!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?`~' for c in password)
    return length_ok, has_upper, has_lower, has_digit, has_special
    
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

        # Real-time checks for password quality
        is_common = is_common_password(data['password'])
        used_personal = check_for_personal_info(data['password'], data)

        if is_common:
            message = 'This password is too common. Please choose a more secure one.'
            return render_template('register.html', message=message, data=data)
        
        # [CHANGED] Logic now checks the ENFORCE_PERSONAL_INFO_CHECK variable
        if used_personal and ENFORCE_PERSONAL_INFO_CHECK:
            message = 'Your password must not contain personal information (like your name, phone, or birthday).'
            return render_template('register.html', message=message, data=data)

        # Hash password and analyze strength
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        length_ok, has_upper, has_lower, has_digit, has_special = get_password_flags(data['password'])

        # Save user and security info
        with open(USER_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([data['fullname'], data['email'], data['phone'], data['department'], data['dob'], data['gender'], data['address']])
        with open(SECURITY_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([data['email'], hashed_pw, str(length_ok).lower(), str(has_upper).lower(), str(has_lower).lower(), str(has_digit).lower(), str(has_special).lower(), str(is_common).lower(), str(used_personal).lower()])

        # [NEW] If not enforcing the check but personal info was used, flash a warning for the next page.
        if used_personal and not ENFORCE_PERSONAL_INFO_CHECK:
            flash('WARNING: Your password contains personal information and is considered insecure. Please consider changing it.', 'warning')
        
        print("[DEBUG] User created successfully")
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
        user_details = {}
        with open(USER_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    user_details = row
                    break
        is_common = is_common_password(new_password_raw)
        used_personal = check_for_personal_info(new_password_raw, user_details)

        if is_common:
            message = 'This new password is too common. Please choose a more secure one.'
            return render_template('reset_password.html', message=message)
        
        # [CHANGED] Logic now checks the ENFORCE_PERSONAL_INFO_CHECK variable
        if used_personal and ENFORCE_PERSONAL_INFO_CHECK:
            message = 'Your new password must not contain personal information.'
            return render_template('reset_password.html', message=message)
        
        rows = []
        updated = False
        length_ok, has_upper, has_lower, has_digit, has_special = get_password_flags(new_password_raw)
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
                        row['common_password'] = str(is_common).lower()
                        row['used_personal_info'] = str(used_personal).lower()
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
            
            # [NEW] If not enforcing, flash a warning. Otherwise, flash success.
            if used_personal and not ENFORCE_PERSONAL_INFO_CHECK:
                flash('WARNING: Your new password contains personal information and is insecure.', 'warning')
            else:
                flash("✅ Password updated successfully.", 'success')
            return redirect(url_for('user.reset_password'))
        else:
            message = "❌ User not found or update failed."
    return render_template('reset_password.html', message=message)

# ---------------------- LOGOUT ----------------------
@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('user.login'))