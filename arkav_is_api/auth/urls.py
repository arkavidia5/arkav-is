from django.urls import path
from .views import (
    SessionView,
    RegistrationView,
    # EmailConfirmationView,  # TODO
    # PasswordResetView,  # TODO
)

urlpatterns = [
    path('', SessionView.as_view()),
    path('register/', RegistrationView.as_view()),
    # path('confirm-email/', EmailConfirmationView.as_view()),  # TODO
    # path('password-reset/', PasswordResetView.as_view()),  # TODO
]
