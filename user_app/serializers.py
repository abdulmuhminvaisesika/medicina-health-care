from rest_framework import serializers
from .models import CustomUser, UserAddress

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'gender', 'phone', 'is_customer', 'is_owner', 'company_name'
        ]

class UserAddressSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'address', 'phone']
