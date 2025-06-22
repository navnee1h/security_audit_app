from flask import Blueprint, render_template, request, redirect, session, url_for
import threading
from app.utils.dashboard_status import is_activated, set_activated

admin_bp = Blueprint('admin', __name__)

# Hardcoded admin credentials (you can change this to use admin.csv if needed)
ADMIN_EMAIL = 'admin'
ADMIN_PASSWORD = 'admin'

@admin_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

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
        return render_template('activate_dashboard.html')  # show loading page

    return render_template('admin_dashboard.html')

@admin_bp.route('/admin/activate-dashboard', methods=['POST'])
def activate_dashboard():
    def background_task():
        print("[DEBUG] Starting password analysis...") # real analyzis here
        import time
        time.sleep(5) # dummy sleep
        set_activated()
        print("[DEBUG] Dashboard activated!")

    threading.Thread(target=background_task).start()
    return '', 200
@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin.admin_login'))
