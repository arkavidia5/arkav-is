from django.urls import path
from .views import (
    ListCompetitionsView,
    RegisterTeamView,
    AddTeamMemberView,
    ConfirmTeamMemberView,
    ListTeamsView,
    RetrieveUpdateDestroyTeamView,
    RetrieveUpdateDestroyTeamMemberView,
    SubmitTaskResponseView,
)

urlpatterns = [
    path('', ListCompetitionsView.as_view()),
    path('register-team/', RegisterTeamView.as_view()),
    path('confirm-team-member/', ConfirmTeamMemberView.as_view()),
    path('teams/', ListTeamsView.as_view()),
    path('teams/<int:team_id>/', RetrieveUpdateDestroyTeamView.as_view()),
    path('teams/<int:team_id>/members/', AddTeamMemberView.as_view()),
    path('teams/<int:team_id>/members/<int:team_member_id>/', RetrieveUpdateDestroyTeamMemberView.as_view()),
    path('teams/<int:team_id>/tasks/<int:task_id>/', SubmitTaskResponseView.as_view()),
]
