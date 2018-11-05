from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = (
            'full_name', 'email',
            'is_staff', 'is_active', 'last_login', 'date_joined',
        )
        read_only_fields = ('last_login', 'date_joined')


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()


class RegistrationRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField()


class EmailConfirmationAttemptSerializer(serializers.Serializer):
    token = serializers.CharField()


class TryPasswordResetAttemptSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetAttemptSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
