from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    Gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=Gender_choices, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)  # Add this field
    company_name = models.CharField(max_length=100, blank=True)

class UserAddress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True)
