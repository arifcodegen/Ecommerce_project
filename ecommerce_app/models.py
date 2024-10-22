from django.db import models
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

# Generate a key (in a real application, store this securely)
def load_key():
    """Load the encryption key from a file."""
    key_path = os.path.join(settings.BASE_DIR, 'encryption_key.key')
    with open(key_path, 'rb') as key_file:
        return key_file.read()

# Create Fernet instance
key = load_key()
cipher = Fernet(key)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.BinaryField()  # Store encrypted data
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def set_price(self, raw_price):
        self.price = cipher.encrypt(str(raw_price).encode())

    def get_price(self):
        try:
            return float(cipher.decrypt(self.price).decode())
        except InvalidToken as e:
            print(f"Decryption failed for product {self.name}: {e}")
            return None
