from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

# Generate a key (in a real application, store this securely)
def generate_key():
    return base64.urlsafe_b64encode(os.urandom(32))

# Create Fernet instance
key = generate_key()
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

    def set_price(self, raw_price):
        self.price = cipher.encrypt(str(raw_price).encode())

    def get_price(self):
        return float(cipher.decrypt(self.price).decode())
