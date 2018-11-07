from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    is_email_confirmed = serializers.BooleanField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = (
            'full_name', 'email',
            'is_staff', 'is_active', 'is_email_confirmed', 'last_login', 'date_joined',
        )
        read_only_fields = ('last_login', 'date_joined')


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegistrationRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=75)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField()


class RegistrationConfirmationRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=30)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmationRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=30)
    new_password = serializers.CharField()


class PasswordChangeRequestSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
