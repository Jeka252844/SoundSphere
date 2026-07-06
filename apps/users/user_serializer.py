from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from users.models import User
from users.validators import PasswordValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'username', 'role', 'is_artist', 'avatar', 'bio')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=8, write_only=True, required = True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        validators = [
            PasswordValidator(field='password')
        ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'username', 'is_active')


class UserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only= True)
    new_password = serializers.CharField(write_only = True, min_length=8, max_length=16, required=True)


class UserTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['email'] = user.email
        return token