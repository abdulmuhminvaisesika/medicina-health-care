from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser
import re


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'gender', 'phone', 'company_name', 'address', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        """Validate that the role is either 'Customer' or 'Owner'."""
        if value not in ['Customer', 'Owner']:
            raise serializers.ValidationError("Role must be either 'Customer' or 'Owner'.")
        return value

    def validate_phone(self, value):
        """Validate phone number format."""
        phone_regex = r'^\+?[0-9]{10,15}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
        
    def validate_email(self, value):
        """Validate that the email is unique."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_password(self, value):
        """Validate the password strength."""
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        """Create and return a new user instance."""
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update and return an existing user instance."""
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance




#serilizer for customer operayions
class CustomerInfo(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'gender', 'phone', 'company_name', 'address']
        extra_kwargs = {
            'password': {'write_only': True},
        }

