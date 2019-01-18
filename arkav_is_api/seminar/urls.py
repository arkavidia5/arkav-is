from django.urls import path

from .views import RegisterView, SeminarPing, SeminarConfiguration, PaymentReceipt

urlpatterns = [
    path('configuration/', SeminarConfiguration.as_view()),
    path('ping/', SeminarPing.as_view()),
    path('register/', RegisterView.as_view()),
    path('pay/', PaymentReceipt.as_view())
]
