from django.urls import path
from .views import (
    get_current_session_view,
    login_view,
    logout_view,
    registration_view,
    EmailConfirmationAttemptView,
    TryPasswordResetAttemptView,
    PasswordResetAttemptView,
)

urlpatterns = [
    path('', get_current_session_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', registration_view),
    path('confirm-email/', EmailConfirmationAttemptView.as_view()),
    path('try-reset-password/', TryPasswordResetAttemptView.as_view()),
    path('reset-password/', PasswordResetAttemptView.as_view()),
]
