from cryptography.fernet import Fernet

# Generate a new key and save it to a file
key = Fernet.generate_key()
with open('encryption_key.key', 'wb') as key_file:
    key_file.write(key)
