#https://crackstation.net/hashing-security.htm#properhashing
#https://stackoverflow.com/questions/5293959/creating-a-salt-in-python
#https://docs.python.org/3/library/secrets.html
#https://docs.python.org/2/library/hashlib.html
import secrets
import hashlib

def generateSalt(length):
    return secrets.token_hex(int(length / 2))

def hashInput(input, salt):
    return hashlib.pbkdf2_hmac('sha256',input,salt,1000)

def validate(input, salt, hash):
    return secrets.compare_digest(hashInput(input,salt),hash)
