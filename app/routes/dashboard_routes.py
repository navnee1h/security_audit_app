import os
import re
import pandas as pd
# ADD session, redirect, and url_for to the imports
from flask import Blueprint, send_from_directory, jsonify, current_app, session, redirect, url_for

# The blueprint for our dashboard.
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# =====================================================================
#  THIS IS THE NEW SECURITY CHECK
# =====================================================================
@dashboard_bp.before_request
def check_admin_session():
    """
    This function runs before EVERY request handled by this blueprint.
    It checks if the 'admin' key is in the session.
    If not, it redirects the user to the login page.
    """
    if 'admin' not in session:
        return redirect(url_for('admin.admin_login'))
# =====================================================================


# --- Route to serve the main index.html file ---
@dashboard_bp.route('/')
def serve_dashboard_index():
    dashboard_dir = os.path.join(current_app.root_path, '..', 'admin_dashboard')
    return send_from_directory(dashboard_dir, 'index.html')

# --- Route to serve all other files (CSS, JS, other HTML pages) ---
@dashboard_bp.route('/<path:filename>')
def serve_dashboard_files(filename):
    dashboard_dir = os.path.join(current_app.root_path, '..', 'admin_dashboard')
    return send_from_directory(dashboard_dir, filename)

# --- The API Endpoint ---
@dashboard_bp.route('/api/data')
def get_dashboard_data():
    try:
        data_dir = os.path.join(current_app.root_path, '..', 'data')
        # ... (the rest of your API code is exactly the same)
        users_df = pd.read_csv(os.path.join(data_dir, 'users.csv'))
        security_df = pd.read_csv(os.path.join(data_dir, 'user_security.csv'))
        
        merged_df = pd.merge(users_df, security_df, on='email', how='left')

        def get_password_status(row):
            if row.get('common_password', False): return "Common"
            if not row.get('length_ok', True) or not row.get('has_upper', True) or not row.get('has_digit', True): return "Weak"
            return "Strong"

        merged_df['password_status'] = merged_df.apply(get_password_status, axis=1)
        users_list = merged_df.to_dict(orient='records')

        status_counts = merged_df['password_status'].value_counts()
        summary_stats = {
            "total_users": int(len(merged_df)),
            "strong_passwords": int(status_counts.get("Strong", 0)),
            "weak_passwords": int(status_counts.get("Weak", 0)),
            "common_passwords": int(status_counts.get("Common", 0)),
        }
        
        def parse_log_file(file_path):
            logs = []
            log_pattern = re.compile(r'\[(.*?)\] (SUCCESS|FAILED) LOGIN: (.*?) from IP: (.*)')
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        match = log_pattern.match(line.strip())
                        if match:
                            logs.append({"timestamp": match.group(1), "status": match.group(2).capitalize(), "email": match.group(3), "ip": match.group(4)})
            except FileNotFoundError:
                pass
            return logs[::-1]

        login_logs = parse_log_file(os.path.join(data_dir, 'login-log.txt'))
        
        return jsonify({"users": users_list, "logs": login_logs, "summary_stats": summary_stats})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
