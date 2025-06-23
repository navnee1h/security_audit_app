from flask import Blueprint, render_template, request, redirect, session, url_for
import threading
from app.utils.dashboard_status import is_activated, set_activated
from app.utils.personal_info_passwords import analyze_personal_passwords

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

@admin_bp.route('/admin/dashboard/view')
def view_dashboard():
    return render_template('admin_dashboard.html')


@admin_bp.route('/admin/activate-dashboard', methods=['POST'])
def activate_dashboard():
    set_activated()
    return ('', 204)

@admin_bp.route('/admin/loading')
def loading_dashboard():
    return render_template('loading.html')


