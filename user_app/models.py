from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    Gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    Role_choices = [
        ('Customer', 'Customer'),
        ('Owner', 'Owner'),
    ]
    role = models.CharField(max_length=10, choices=Role_choices, blank=True, default='Customer')
    gender = models.CharField(max_length=10, choices=Gender_choices, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_customer = models.BooleanField(default=False)

    is_owner = models.BooleanField(default=False)  # Add this field
    company_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)



    def save(self, *args, **kwargs):
        #according to the role set the is_customer or is_owner
        if self.role == 'Customer':
            self.is_customer = True
            self.is_owner = False
        elif self.role == 'Owner':
            self.is_owner = True
            self.is_customer = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

            
