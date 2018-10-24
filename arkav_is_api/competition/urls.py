from django.urls import path
from .views import (
    ListCompetitionsView,
    RegisterTeamView,
    JoinTeamView,
    ListTeamsView,
    RetrieveUpdateTeamView,
    RetrieveUpdateDestroyTeamMemberView,
    SubmitTaskResponseView,
)

urlpatterns = [
    path('', ListCompetitionsView.as_view()),
    path('register-team/', RegisterTeamView.as_view()),
    path('join-team/', JoinTeamView.as_view()),
    path('teams/', ListTeamsView.as_view()),
    path('teams/<int:team_id>/', RetrieveUpdateTeamView.as_view()),
    path('teams/<int:team_id>/members/<str:username>/', RetrieveUpdateDestroyTeamMemberView.as_view()),
    path('teams/<int:team_id>/tasks/<int:task_id>/', SubmitTaskResponseView.as_view()),
]
