from itertools import product

# --- Helper functions to generate word variations ---
def modify_word(word):
    # Returns a word in lowercase and Titlecase
    return list(set([word.lower(), word.title()]))

def get_combinations(text_block):
    # Creates combinations from a string like "Test User" -> ["testuser", "TestUser", ...]
    if not text_block or not isinstance(text_block, str):
        return []
    
    words_to_combine = [modify_word(w) for w in text_block.split()]
    # Use product to create all combinations, e.g., ('Test', 'User'), ('test', 'user'), etc.
    return [''.join(p) for p in product(*words_to_combine)]

# --- Main Functions ---

def generate_wordlist(user_row):
    """
    Creates a list of "suspect words" based on a user's personal information.
    """
    words = set() # Use a set to handle duplicates automatically

    # Add combinations from various text fields
    words.update(get_combinations(user_row.get('fullname')))
    if user_row.get('email'):
        words.update(get_combinations(user_row['email'].split("@")[0]))
    words.update(get_combinations(user_row.get('address')))
    words.update(get_combinations(user_row.get('department')))
    
    # Add date variations
    if user_row.get('dob'):
        words.add(user_row['dob'].replace("-", ""))
    
    # Add phone number variations
    if user_row.get('phone'):
        phone = user_row['phone']
        words.add(phone)
        if len(phone) >= 4:
            words.add(phone[-4:])
            words.add(phone[:4])
            
    # Return a list of unique words with a minimum length
    return [word for word in words if len(word) >= 4]

def check_for_personal_info(password, user_row):
    """
    Checks if a plaintext password contains any words from the user's personal wordlist.
    Returns True if personal info is found, False otherwise.
    """
    personal_words = generate_wordlist(user_row)
    password_lower = password.lower()

    for word in personal_words:
        if word.lower() in password_lower:
            # Found a personal word inside the password
            return True
            
    # No personal words were found
    return False