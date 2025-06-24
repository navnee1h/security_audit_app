import csv
import os
import bcrypt
from itertools import product
#---------------------- WANT TO IMPROVE THIS [CORRECT THE LOGIC]-----------------------------
def modify_word(word):
    return [word.lower(), word.title()]

def remove_duplicates(modified_array):
    seen = set()
    return [[w for w in words if w not in seen and not seen.add(w)] for words in modified_array]

def get_combinations(word):
    if not word:
        return []
    modified = [modify_word(w) for w in word.split()]
    clean = remove_duplicates(modified)
    return [''.join(p) for p in product(*clean)] if clean else []

def generate_wordlist(user_row):
    words = []
    words += get_combinations(user_row['fullname'])
    words += get_combinations(user_row['email'].split("@")[0])
    words += get_combinations(user_row['address'])
    words += get_combinations(user_row['department'])
    words += get_combinations(user_row['dob'].replace("-", ""))
    words += [user_row['phone'], user_row['phone'][-4:], user_row['phone'][:4]]
    return list(set(filter(lambda x: len(x) >= 4, words)))  # unique and length check

def analyze_personal_passwords(users_csv_path, user_security_csv_path, rules_txt_path, output_path):
    with open(users_csv_path, 'r') as user_file, open(user_security_csv_path, 'r') as sec_file:
        users = list(csv.DictReader(user_file))
        security = list(csv.DictReader(sec_file))

    updated_rows = []
    for sec_row in security:
        email = sec_row['email']
        hashed_password = sec_row['password']
        matching_user = next((u for u in users if u['email'] == email), None)
        if not matching_user:
            continue
        wordlist = generate_wordlist(matching_user)

        used_personal_info = False
        for word in wordlist:
            if bcrypt.checkpw(word.encode(), hashed_password.encode()):
                used_personal_info = True
                break

        sec_row['used_personal_info'] = str(used_personal_info).lower()
        updated_rows.append(sec_row)

    fieldnames = updated_rows[0].keys()
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"[INFO] Analysis complete. Result saved to {output_path}")
