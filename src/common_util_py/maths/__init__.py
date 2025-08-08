import re

def is_prime(n):
    return re.match(r'^1?$|^(11+?)\1+$',"1"*n) is None
