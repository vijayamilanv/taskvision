from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'first_name', 'last_name', 
                 'company', 'industry', 'specialization', 'years_experience', 'skills', 'experience_level',
                 'points', 'streak', 'productivity_score']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone', 'first_name', 'last_name', 
                 'company', 'industry', 'specialization', 'years_experience', 'skills', 'experience_level']

    def create(self, validated_data):
        # Extract password before creating user
        password = validated_data.pop('password')
        
        # Create user without password first
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create token for authentication
        Token.objects.create(user=user)
        
        return user
