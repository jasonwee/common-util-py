import re

def is_valid(email_str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email_str):
        return True
    return False

