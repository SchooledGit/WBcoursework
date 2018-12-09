# https://crackstation.net/hashing-security.htm#properhashing
# https://stackoverflow.com/questions/5293959/creating-a-salt-in-python
# https://docs.python.org/3/library/secrets.html
# https://docs.python.org/2/library/hashlib.html
# https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
# https://python-forum.io/Thread-how-to-convert-a-string-to-hex
import secrets
import hashlib


def generateSalt(length):
    output = secrets.token_hex(int(length / 2))
    return output


def hashInput(input, salt):
    output = hashlib.sha512(input.encode('utf-8') +
                            salt.encode('utf-8')).hexdigest()
    return output


def validate(password, salt, hash):
    return secrets.compare_digest(hash, hashInput(password, salt))
