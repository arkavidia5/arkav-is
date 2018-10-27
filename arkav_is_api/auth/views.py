from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from .serializers import (
    UserSerializer,
    LoginRequestSerializer,
    RegistrationRequestSerializer,
)

# TODO: tests
# TODO: request throttling/rate limiting
# TODO: captcha for registration, email verification and password reset


class SessionView(views.APIView):
    def has_permission(self, request, view):
        if request.method in ['GET', 'DELETE']:
            return request.user and request.user.is_authenticated()
        else:
            return True

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        """
        Get the current user and CSRF token.
        """
        response_serializer = UserSerializer(request.user)
        return Response(data=response_serializer.data)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        """
        Login.
        """
        request_serializer = LoginRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=request_serializer.validated_data['username'],
            password=request_serializer.validated_data['password'],
        )
        if user is None:
            return Response(
                {
                    'code': 'login_failed',
                    'detail': 'Wrong username or password.',
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        response_serializer = UserSerializer(request.user)
        return Response(data=response_serializer.data)

    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, format=None):
        """
        Logout.
        """
        logout(request)
        return Response()


class RegistrationView(views.APIView):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        """
        User registration.
        """
        request_serializer = RegistrationRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = User.objects.create_user(
                username=request_serializer.validated_data['username'],
                email=request_serializer.validated_data['email'],
                password=request_serializer.validated_data['password'],
            )
            user.first_name = request_serializer.validated_data['first_name'],
            user.last_name = request_serializer.validated_data['last_name'],
            user.save()

        # Login the user after registration
        login(request, user)
        response_serializer = UserSerializer(request.user)
        return Response(data=response_serializer.data)
