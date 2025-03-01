from django.contrib.auth import get_user_model
from .models import WishList
from rest_framework import serializers, status
from rest_framework.response import Response

User = get_user_model()

class RegisterSerialzier(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'date_of_birth', 'gender', 'username']

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email
    
    def validate_phone_number(self, phone_number):
        if len(phone_number) < 11:
            raise serializers.ValidationError("Invalid phone number")
        return phone_number
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'date_of_birth', 'gender', 'username']
    
    def validate_email(self, email):
        if self.instance.email != email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email
    
    def validate_phone_number(self, phone_number):
        if len(phone_number) < 11:
            raise serializers.ValidationError("Invalid phone number")
        return phone_number
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'date_of_birth', 'gender', 'username']


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['product', 'created_at', 'updated_at', 'name', 'id', 'user']
        extra_kwargs = {'user': {'write_only': True}}
        
    def save(self, **kwargs):
        user = self.context['request'].user
        self.validated_data['user'] = user
        return super().save(**kwargs)