from flask import Blueprint, render_template, request, redirect, url_for, session
import csv, os, bcrypt

user_bp = Blueprint('user', __name__)
USER_CSV = 'data/users.csv'
SECURITY_CSV = 'data/user_security.csv'

# Ensure both CSVs exist
for csv_file, headers in [
    (USER_CSV, ['fullname', 'email', 'phone', 'dob', 'gender', 'address']),
    (SECURITY_CSV, ['email', 'password', 'password_status', 'audit_warning'])
]:
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        data = {
            'fullname': request.form['fullname'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'dob': request.form['dob'],
            'gender': request.form['gender'],
            'address': request.form['address'],
            'password': request.form['password']
        }

        # Password hashing
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Save personal info to users.csv
        with open(USER_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['fullname'], data['email'], data['phone'],
                data['dob'], data['gender'], data['address']
            ])

        # Save security info to user_security.csv
        with open(SECURITY_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['email'], hashed_pw, 'unchecked', 'false'
            ])

        return redirect(url_for('user.login'))

    return render_template('register.html', message=message)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password'].encode('utf-8')

        # Step 1: Authenticate using user_security.csv
        authenticated = False
        with open(SECURITY_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    stored_hash = row['password'].encode('utf-8')
                    if bcrypt.checkpw(password_input, stored_hash):
                        authenticated = True
                    break

        if authenticated:
            # Step 2: Fetch user's full name from users.csv
            with open(USER_CSV, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['email'] == email:
                        session['user'] = row['fullname']
                        return f"Welcome {row['fullname']}! (Later you'll redirect to dashboard)"
            # Fallback in case name not found
            session['user'] = email
            return f"Welcome {email}! (Later you'll redirect to dashboard)"
        else:
            message = "Invalid email or password."

    return render_template('login.html', message=message)

