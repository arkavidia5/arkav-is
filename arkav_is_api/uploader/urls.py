from django.urls import path
from .views import upload_file_view

urlpatterns = [
    path('', upload_file_view),
]
