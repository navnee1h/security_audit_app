import os, json

STATUS_FILE = 'data/dashboard_status.json'

def is_activated():
    if not os.path.exists(STATUS_FILE):
        return False
    with open(STATUS_FILE, 'r') as f:
        status = json.load(f)
    return status.get("activated", False)

def set_activated():
    with open(STATUS_FILE, 'w') as f:
        json.dump({"activated": True}, f)
