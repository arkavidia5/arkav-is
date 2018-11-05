from django.urls import path
from .views import upload_file_view, download_file_view

urlpatterns = [
    path('', upload_file_view, name='upload'),
    path('download/<uuid:file_id>/', download_file_view, name='download'),
]
