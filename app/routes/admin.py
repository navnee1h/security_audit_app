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

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin.admin_login'))

    if not is_activated():
        return render_template('activate_dashboard.html')

    # Run background analysis every time after activation
    def background_task():
        users_csv = 'data/users.csv'
        security_csv = 'data/user_security.csv'
        output_csv = 'data/user_security.csv'
        rules_txt = 'app/utils/patterns/rules.txt'
        print("[DEBUG] Background password analysis (on dashboard visit)...")
        analyze_personal_passwords(users_csv, security_csv, rules_txt, output_csv)

    threading.Thread(target=background_task).start()

    # Show loading animation before final dashboard
    return render_template('loading_dashboard.html')




@admin_bp.route('/admin/dashboard/view')
def view_dashboard():
    return render_template('admin_dashboard.html')


@admin_bp.route('/admin/activate-dashboard', methods=['POST'])
def activate_dashboard():
    set_activated()
    
    # Run analysis immediately after activation
    def background_task():
        print("[DEBUG] First-time activation analysis...")
        users_csv = 'data/users.csv'
        security_csv = 'data/user_security.csv'
        output_csv = 'data/user_security.csv'
        rules_txt = 'app/utils/patterns/rules.txt'
        analyze_personal_passwords(users_csv, security_csv, rules_txt, output_csv)
        print("[DEBUG] First-time dashboard activated.")

    threading.Thread(target=background_task).start()
    return ('', 204)

@admin_bp.route('/admin/loading')
def loading_dashboard():
    return render_template('loading.html')

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin.admin_login'))
