from django.urls import path

from .views import QuizAttemptView, QuizQuickSaveView, QuizSaveView

urlpatterns = [
    path('<slug:quiz_slug>/latest', QuizAttemptView.as_view()),
    path('<slug:quiz_slug>/latest/finish', QuizSaveView.as_view()),
    path('<slug:quiz_slug>/latest/quicksave', QuizQuickSaveView.as_view()),
]
