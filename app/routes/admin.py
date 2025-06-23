from flask import Blueprint, render_template, request, redirect, session, url_for
import threading
from app.utils.dashboard_status import is_activated, set_activated
from app.utils.password_analysis import analyze_personal_passwords

admin_bp = Blueprint('admin', __name__)

# Hardcoded admin credentials
ADMIN_EMAIL = 'admin'
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

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin.admin_login'))

    if not is_activated():
        def background_task():
            print("[DEBUG] Starting personal password analysis...")
            users_csv = 'data/users.csv'
            security_csv = 'data/user_security.csv'
            output_csv = 'data/user_security.csv'
            rules_txt = 'app/utils/patterns/rules.txt'

            analyze_personal_passwords(users_csv, security_csv, rules_txt, output_csv)
            set_activated()  # Set JSON flag after completion
            print("[DEBUG] Dashboard activated!")

        threading.Thread(target=background_task).start()
        return render_template('activate_dashboard.html')  # Show loading screen

    return render_template('admin_dashboard.html')  # Show dashboard

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin.admin_login'))
