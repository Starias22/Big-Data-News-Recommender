import hashlib

def encrypt_password(password):
    password = password.encode('utf-8')  # Convert the password to bytes
    encrypted_passwd = hashlib.sha256(password).hexdigest()
    return encrypted_passwd

def is_empty(text):
    return text==None or text==''