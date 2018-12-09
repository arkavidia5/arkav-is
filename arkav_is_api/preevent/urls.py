from django.urls import path

from .views import CodingClass, RegistrationPing

urlpatterns = [
    path('codingclass', CodingClass.as_view()),
    path('ping', RegistrationPing.as_view()),
]
