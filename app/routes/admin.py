from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify 
import threading
from app.utils.dashboard_status import is_activated, set_activated
import csv                      # <-- For writing to the csv file
from datetime import datetime   # <-- For getting the timestamp

admin_bp = Blueprint('admin', __name__)

# Hardcoded admin credentials
ADMIN_EMAIL = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin'

@admin_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    message = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin.admin_dashboard'))
        else:
            message = "Invalid admin credentials."
    return render_template('admin_login.html', message=message)


@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin.admin_login'))


@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin.admin_login'))

    if not is_activated():
        return render_template('activate_dashboard.html')
    # DO ANY ARRANGEMENT OF DATA FOR SHOWING IT ON DASHBOARD-->ON BACKGROUND(THREADING)
    print("arrangement of data to dashboard goes here") #--------------
    # Show loading animation before final dashboard
    return render_template('loading_dashboard.html')

#@admin_bp.route('/admin/dashboard/view')
#def view_dashboard():
#   return render_template('admin_dashboard.html')


@admin_bp.route('/admin/activate-dashboard', methods=['POST'])
def activate_dashboard():
    # This function now returns a JSON object, which the front-end can understand.
    set_activated()
    return jsonify(status="success", message="Activation complete!")

@admin_bp.route('/admin/loading')
def loading_dashboard():
    return render_template('loading.html')
@admin_bp.route('/admin/notify', methods=['POST'])
def notify_user():
    """
    Receives a notification request from the admin dashboard and logs it.
    """
    if not session.get('admin'):
        return jsonify(status="error", message="Unauthorized"), 401

    data = request.get_json()
    email = data.get('email')
    reason = data.get('reason')

    if not email or not reason:
        return jsonify(status="error", message="Missing email or reason"), 400

    # Log the notification to our new CSV file
    with open('data/notifications.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Format: email, message, reason, timestamp, is_read
        writer.writerow([email, "Password reset required", reason, timestamp, "false"])
    
    # Send a success response back to the JavaScript
    return jsonify(status="success", message=f"Notification sent to {email}.")

