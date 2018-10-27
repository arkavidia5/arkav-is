from django.urls import path
from .views import (
    get_current_session_view,
    login_view,
    logout_view,
    registration_view,
    # EmailConfirmationView,  # TODO
    # PasswordResetView,  # TODO
)

urlpatterns = [
    path('', get_current_session_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', registration_view),
    # path('confirm-email/', EmailConfirmationView.as_view()),  # TODO
    # path('password-reset/', PasswordResetView.as_view()),  # TODO
]
