def is_common_password(password, weak_passwords_path='app/utils/patterns/weak_passwords.txt'):
    print("Checking weak_passwords is called!")
    try:
        with open(weak_passwords_path, 'r') as f:
            weak_passwords = set(line.strip().lower() for line in f)
        return password.lower() in weak_passwords
    except FileNotFoundError:
        print("[ERROR] weak.txt not found.")
        return False
