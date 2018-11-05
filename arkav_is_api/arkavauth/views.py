from rest_framework import permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError
from .models import User, EmailConfirmationAttempt, PasswordResetAttempt
from .serializers import (
    UserSerializer,
    LoginRequestSerializer,
    RegistrationRequestSerializer,
    EmailConfirmationAttemptSerializer,
    TryPasswordResetAttemptSerializer,
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
                'detail': 'Wrong email or password.',
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.email_confirmed:
        return Response(
            {
                'code': 'not_confirmed_account',
                'detail': 'Account email hasn\'t been confirmed. Check inbox for confirmation email',
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
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                email=request_serializer.validated_data['email'],
                password=request_serializer.validated_data['password'],
                full_name=request_serializer.validated_data['full_name'],
            )
            user.save()

            attempt, _ = EmailConfirmationAttempt.objects.get_or_create(user=user)
            attempt.send_email()
    except IntegrityError:
        return Response({
            'code': 'error',
            'detail': 'Email has been already used'
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'code': 'registered',
        'detail': 'Email confirmation link has been sent to your email.'
    })


class EmailConfirmationAttemptView(views.APIView):

    def post(self, request):
        request_serializer = EmailConfirmationAttemptSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        token = request_serializer.validated_data['token']

        attempt = EmailConfirmationAttempt.objects.filter(token=token).first()

        if attempt is None:
            return Response({
                'code': 'invalid_token',
                'detail': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if attempt.confirmed or attempt.user.email_confirmed:
            return Response({
                'code': 'already_confirmed',
                'detail': 'Email has been already confirmed.'
            }, status=status.HTTP_400_BAD_REQUEST)

        attempt.confirm()

        return Response({
            'code': 'ok',
            'detail': 'Your email has been successfully confirmed.'
        })


class TryPasswordResetAttemptView(views.APIView):

    def post(self, request):
        request_serializer = TryPasswordResetAttemptSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        email = request_serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user is not None:
            attempt, _ = PasswordResetAttempt.objects.get_or_create(user=user)
            attempt.generate_new_token()
            attempt.send_email()
            attempt.save()

        return Response({
            'code': 'ok',
            'detail':
                'If you have registered using that email, we have sent password reset link to your email.'
                ' Please check your email.'
        })


class PasswordResetAttemptView(views.APIView):

    def post(self, request):
        request_serializer = PasswordResetAttemptSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        token = request_serializer.validated_data['token']

        attempt = PasswordResetAttempt.objects.filter(token=token).first()

        if attempt is None or attempt.used:
            return Response({
                'code': 'invalid_token',
                'detail': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = attempt.user
        with transaction.atomic():
            attempt.used = True
            attempt.save()

            user.set_password(request_serializer.validated_data['password'])
            user.save()

        return Response({
            'code': 'ok',
            'detail': 'Reseted.'})
