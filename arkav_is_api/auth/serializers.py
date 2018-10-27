from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'is_staff', 'is_active', 'last_login', 'date_joined',
        )
        read_only_fields = ('last_login', 'date_joined')


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class RegistrationRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_username(self, value):
        User.username_validator(value)
        return value
