"""arkav_is_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from arkav_is_api.competition.views import FileView

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),

    # API routes
    path('api/auth/', include('arkav_is_api.arkavauth.urls')),
    path('api/competitions/', include('arkav_is_api.competition.urls')),

    # File upload routes
    path('file/', FileView.as_view()),
    path('file/<str:slug>/', FileView.as_view()),
]
