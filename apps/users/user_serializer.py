from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from apps.users.models import User
from apps.users.validators import PasswordValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'username', 'user_role', 'is_artist', 'avatar', 'bio')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=8, write_only=True, required = True)
    email = serializers.EmailField(required = True)
    phone_number = serializers.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number', 'user_role', 'is_active', 'is_artist')
        extra_kwargs = {
            "password": {
                "max_length":16, 
                "min_length":8, 
                "write_only":True, 
                "required": True},
            "email": {"required": False},
            "phone_number": {"required": False}
        }

        validators = [
            PasswordValidator(field='password')
        ]
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Этот email уже используется')
        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'username', 'user_role', 'is_active', 'is_artist')


class UserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only= True)
    new_password = serializers.CharField(write_only = True, min_length=8, max_length=16, required=True)