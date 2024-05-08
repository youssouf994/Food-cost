import os

def generate_secret_key():
    return os.urandom(24).hex()

secret_key = generate_secret_key()
print(secret_key)

