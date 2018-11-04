from rest_framework import permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .models import User, EmailConfirmationAttempt, PasswordResetAttempt
from .serializers import (
    UserSerializer,
    LoginRequestSerializer,
    RegistrationRequestSerializer,
    EmailConfirmationAttemptSerializer,
    PasswordResetAttemptSerializer,
)


# TODO: tests
# TODO: request throttling/rate limiting
# TODO: captcha for registration, email verification and password reset


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user) or (not request.user.is_authenticated)


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_current_session_view(request):
    response_serializer = UserSerializer(request.user)
    return Response(data=response_serializer.data)


@ensure_csrf_cookie
@sensitive_post_parameters('password')
@api_view(['POST'])
@permission_classes((IsNotAuthenticated, ))
def login_view(request):
    request_serializer = LoginRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)

    user = authenticate(
        email=request_serializer.validated_data['email'],
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


@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def logout_view(request):
    logout(request)
    return Response()


@ensure_csrf_cookie
@sensitive_post_parameters('password')
@api_view(['POST'])
@permission_classes((IsNotAuthenticated, ))
def registration_view(request):
    request_serializer = RegistrationRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    with transaction.atomic():
        user = User.objects.create_user(
            email=request_serializer.validated_data['email'],
            password=request_serializer.validated_data['password'],
            full_name=request_serializer.validated_data['full_name'],
        )
        user.save()

    # Login the user after registration
    login(request, user)
    response_serializer = UserSerializer(request.user)
    return Response(data=response_serializer.data)


class TryEmailConfirmationAttemptView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        user = request.user

        if user.email_confirmed:
            return Response(data={'status': 'already confirmed'}, status=400)

        attempt, _ = EmailConfirmationAttempt.objects.get_or_create(user=user)
        attempt.send_email()

        return Response(data={'status': 'ok', 'token': attempt.token})


class EmailConfirmationAttemptView(views.APIView):

    def post(self, request):
        request_serializer = EmailConfirmationAttemptSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        token = request_serializer.validated_data['token']

        attempt = EmailConfirmationAttempt.objects.filter(token=token).first()

        if attempt is None:
            return Response(data={'status': 'wrong token'}, status=400)

        if attempt.confirmed or attempt.user.email_confirmed:
            return Response(data={'status': 'already confirmed'}, status=400)

        attempt.confirm()

        return Response(data={'status': 'confirmed'})


class TryPasswordResetAttemptView(views.APIView):

    def post(self, request):
        user = request.user

        attempt, _ = PasswordResetAttempt.objects.get_or_create(user=user)
        attempt.generate_new_token()
        attempt.send_email()
        attempt.save()

        return Response(data={'status': 'ok'})


class PasswordResetAttemptView(views.APIView):

    def post(self, request):
        request_serializer = PasswordResetAttemptSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        token = request_serializer.validated_data['token']

        attempt = PasswordResetAttempt.objects.get(token=token)

        if attempt is None or attempt.used:
            return Response(data={'status': 'wrong token'}, status=400)

        user = request.user
        with transaction.atomic():
            attempt.used = True
            attempt.save()

            user.set_password(request_serializer.validated_data['password'])
            user.save()

        return Response(data={'status': 'reseted'})
