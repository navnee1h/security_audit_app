from flask import Blueprint, render_template, request, redirect, url_for, session
import csv, os, bcrypt

user_bp = Blueprint('user', __name__)
USER_CSV = 'data/users.csv'
SECURITY_CSV = 'data/user_security.csv'

# Ensure both CSVs exist
for csv_file, headers in [
    (USER_CSV, ['fullname', 'email', 'phone','department', 'dob', 'gender', 'address']),
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
            'department': request.form['department'],
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
                data['fullname'], data['email'], data['phone'],data['department'],
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



@user_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    # ✅ Require login
    if 'user' not in session or 'email' not in session:
        return redirect(url_for('user.login'))

    message = ''

    if request.method == 'POST':
        email = session['email']
        old_password = request.form['old_password'].encode('utf-8')
        new_password = request.form['new_password'].encode('utf-8')

        rows = []
        updated = False

        # ✅ Read existing records
        with open(SECURITY_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Match the current user's record
                if row['email'] == email:
                    # Check if old password is correct
                    if bcrypt.checkpw(old_password, row['password'].encode('utf-8')):
                        # Update the password with new hashed value
                        hashed = bcrypt.hashpw(new_password, bcrypt.gensalt())
                        row['password'] = hashed.decode('utf-8')
                        row['password_status'] = 'unchecked'
                        row['audit_warning'] = 'false'
                        updated = True
                    else:
                        message = "❌ Old password is incorrect."
                        return render_template('reset_password.html', message=message)
                rows.append(row)

        # ✅ Write updated records back to CSV
        if updated:
            with open(SECURITY_CSV, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            message = "✅ Password updated successfully."
        else:
            message = "❌ User not found or update failed."

    return render_template('reset_password.html', message=message)
@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('user.login'))

