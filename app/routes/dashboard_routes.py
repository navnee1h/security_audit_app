import os
import re
import pandas as pd
from flask import Blueprint, send_from_directory, jsonify, current_app, session, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.before_request
def check_admin_session():
    if 'admin' not in session:
        return redirect(url_for('admin.admin_login'))

@dashboard_bp.route('/')
def serve_dashboard_index():
    dashboard_dir = os.path.join(current_app.root_path, '..', 'admin_dashboard')
    return send_from_directory(dashboard_dir, 'index.html')

@dashboard_bp.route('/<path:filename>')
def serve_dashboard_files(filename):
    dashboard_dir = os.path.join(current_app.root_path, '..', 'admin_dashboard')
    return send_from_directory(dashboard_dir, filename)

@dashboard_bp.route('/api/data')
def get_dashboard_data():
    try:
        data_dir = os.path.join(current_app.root_path, '..', 'data')
        users_df = pd.read_csv(os.path.join(data_dir, 'users.csv'))
        security_df = pd.read_csv(os.path.join(data_dir, 'user_security.csv'))
        
        # Convert boolean strings from CSV to actual booleans for easier processing
        for col in ['length_ok', 'has_upper', 'has_lower', 'has_digit', 'has_special', 'common_password', 'used_personal_info']:
            if col in security_df.columns:
                 # Map 'true'/'True' to True, everything else to False
                security_df[col] = security_df[col].astype(str).str.lower() == 'true'

        merged_df = pd.merge(users_df, security_df, on='email', how='left')

        # [THIS FUNCTION IS NOW FIXED]
        def get_password_status(row):
            """Determines the overall password risk, now including personal info check."""
            if row.get('common_password', False):
                return "Common"
            
            # A password is 'Weak' if it fails complexity OR uses personal info
            if not row.get('length_ok', True) or \
               not row.get('has_upper', True) or \
               not row.get('has_digit', True) or \
               row.get('used_personal_info', False): # <-- THE IMPORTANT ADDED CHECK
                return "Weak"
            
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