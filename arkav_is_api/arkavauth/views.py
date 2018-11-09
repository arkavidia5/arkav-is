from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .models import (
    User,
    RegistrationConfirmationAttempt,
    PasswordResetConfirmationAttempt,
)
from .serializers import (
    UserSerializer,
    LoginRequestSerializer,
    RegistrationRequestSerializer,
    RegistrationConfirmationRequestSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmationRequestSerializer,
    PasswordChangeRequestSerializer,
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
def login_view(request):
    request_serializer = LoginRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)

    user = authenticate(
        email=request_serializer.validated_data['email'].lower(),
        password=request_serializer.validated_data['password'],
    )
    if user is None:
        return Response(
            {
                'code': 'login_failed',
                'detail': 'Wrong email or password.',
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_email_confirmed:
        return Response(
            {
                'code': 'account_email_not_confirmed',
                'detail': 'Account email hasn\'t been confirmed. Check inbox for confirmation email.',
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
            email=request_serializer.validated_data['email'].lower(),
            password=request_serializer.validated_data['password'],
            full_name=request_serializer.validated_data['full_name'],
        )

        attempt = RegistrationConfirmationAttempt.objects.create(user=user)
        attempt.send_email()

    return Response({
        'code': 'registration_succesful',
        'detail': 'Email confirmation link has been sent to your email.'
    })


@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes((IsNotAuthenticated, ))
def registration_confirmation_view(request):
    request_serializer = RegistrationConfirmationRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    token = request_serializer.validated_data['token']

    with transaction.atomic():
        attempt = RegistrationConfirmationAttempt.objects.filter(token=token).first()
        if attempt is None:
            return Response({
                'code': 'invalid_token',
                'detail': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not attempt.is_confirmed:
            attempt.user.is_email_confirmed = True
            attempt.is_confirmed = True
            attempt.save()

    return Response({
        'code': 'registration_confirmation_succesful',
        'detail': 'Your email has been succesfully confirmed.'
    })


@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes((IsNotAuthenticated, ))
def password_reset_view(request):
    request_serializer = PasswordResetRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    email = request_serializer.validated_data['email'].lower()

    with transaction.atomic():
        user = User.objects.filter(email=email).first()
        if user is not None:
            # Overwrite existing password reset confirmation attempt, if present
            if hasattr(user, 'password_reset_confirmation_attempt'):
                user.password_reset_confirmation_attempt.delete()
            attempt = PasswordResetConfirmationAttempt.objects.create(user=user)
            attempt.send_email()

    return Response({
        'code': 'password_reset_email_sent',
        'detail':
            'If you have registered using that email, we have sent password reset link to your email.'
            ' Please check your email.'
    })


@ensure_csrf_cookie
@sensitive_post_parameters('new_password')
@api_view(['POST'])
@permission_classes((IsNotAuthenticated, ))
def password_reset_confirmation_view(request):
    request_serializer = PasswordResetConfirmationRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    token = request_serializer.validated_data['token']
    new_password = request_serializer.validated_data['new_password']

    with transaction.atomic():
        attempt = PasswordResetConfirmationAttempt.objects.filter(token=token).first()
        if attempt is None:
            return Response({
                'code': 'invalid_token',
                'detail': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if attempt.is_confirmed:
            return Response({
                'code': 'token_used',
                'detail': 'This token has been used.'
            }, status=status.HTTP_400_BAD_REQUEST)

        attempt.user.set_password(new_password)
        # Also confirm this user's email, for backward compatibility
        attempt.user.is_email_confirmed = True
        attempt.user.save()
        attempt.is_confirmed = True
        attempt.save()

    return Response({
        'code': 'password_reset_succesful',
        'detail': 'Your password has been succesfully reset.'
    })


@sensitive_post_parameters('password', 'new_password')
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def password_change_view(request):
    request_serializer = PasswordChangeRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    password = request_serializer.validated_data['password']
    new_password = request_serializer.validated_data['new_password']

    if not request.user.check_password(password):
        return Response(
            {
                'code': 'password_change_failed',
                'detail': 'Wrong old password.',
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    request.user.set_password(new_password)
    request.user.save()

    return Response({
        'code': 'password_change_succesful',
        'detail': 'Your password has been changed.'
    })


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def edit_user_view(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
