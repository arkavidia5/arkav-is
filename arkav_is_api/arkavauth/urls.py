from django.urls import path
from .views import (
    get_current_session_view,
    login_view,
    logout_view,
    registration_view,
    registration_confirmation_view,
    password_reset_view,
    password_reset_confirmation_view,
    password_change_view,
    edit_user_view,
)

urlpatterns = [
    path('', get_current_session_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', registration_view),
    path('confirm-registration/', registration_confirmation_view),
    path('reset-password/', password_reset_view),
    path('confirm-password-reset/', password_reset_confirmation_view),
    path('change-password/', password_change_view),
    path('edit-user/', edit_user_view),
]
