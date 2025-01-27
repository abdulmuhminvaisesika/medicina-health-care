from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'phone', 'is_customer', 'is_owner', 'company_name']
    