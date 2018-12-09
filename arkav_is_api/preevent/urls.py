from django.urls import path

from .views import CodingClass

urlpatterns = [
    path('codingclass', CodingClass.as_view()),
]
