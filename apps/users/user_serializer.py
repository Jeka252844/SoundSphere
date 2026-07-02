from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from users.models import User
from users.validators import PasswordValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = ('id', 'email', 'phone_number', 'last_name', 'first_name', 'email', 'role', 'is_artist', 'avatar', 'bio')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=8, write_only=True, reqired = True)

    class Meta:
        models = User
        fields = ('password', 'email')

        validators = [
            PasswordValidator(field='password')
        ]

