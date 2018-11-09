from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from arkav_is_api.arkavauth.models import User
from .models import (
    Competition,
    Team,
    TeamMember,
    Task,
    TaskResponse,
)
from .serializers import (
    CompetitionSerializer,
    RegisterTeamRequestSerializer,
    AddTeamMemberRequestSerializer,
    ConfirmTeamMemberRequestSerializer,
    TeamSerializer,
    TeamDetailsSerializer,
    TeamMemberSerializer,
    TaskResponseSerializer,
)

# TODO: tests
# TODO: request throttling/rate limiting


class ListCompetitionsView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = (IsAuthenticated,)


class RegisterTeamView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request_serializer = RegisterTeamRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        competition = request_serializer.validated_data['competition_id']
        team_name = request_serializer.validated_data['name']
        team_category = request_serializer.validated_data['category']
        team_institution = request_serializer.validated_data['institution']

        # Only register if registration is open for this competition
        if competition.is_registration_open:
            with transaction.atomic():

                # A user can't register in a competition if he/she already participated in the same competition
                if TeamMember.objects.filter(team__competition=competition, user=request.user).exists():
                    return Response({
                        'code': 'competition_already_registered',
                        'detail': 'One user can only participate in one team per competition.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Create a new team led by the current user
                new_team = Team.objects.create(
                    competition=competition,
                    name=team_name,
                    category=team_category,
                    institution=team_institution,
                    team_leader=request.user
                )

                # Add the current user as team member
                TeamMember.objects.create(
                    team=new_team,
                    user=request.user,
                    invitation_full_name=request.user.full_name,
                    invitation_email=request.user.email,
                )

                response_serializer = TeamSerializer(new_team)
                return Response(data=response_serializer.data)
        else:
            return Response({
                'code': 'competition_registration_closed',
                'detail': 'The competition you are trying to register to is not open for registration.'
            }, status=status.HTTP_400_BAD_REQUEST)


class AddTeamMemberView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request_serializer = AddTeamMemberRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        full_name = request_serializer.validated_data['full_name']
        email = request_serializer.validated_data['email']

        with transaction.atomic():
            team = get_object_or_404(Team.objects.all, team__id=self.kwargs['team_id'])
            self.check_object_permissions(self.request, team)

            # Check whether registration is open for this competition
            if not team.competition.is_registration_open:
                return Response({
                    'code': 'competition_registration_closed',
                    'detail': 'The competition you are trying to register to is not open for registration.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check whether this team is full
            if team.team_members.count() >= team.competition.max_team_members:
                return Response({
                    'code': 'team_full',
                    'detail': 'You have exceeded the maximum team members limit.'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                member_user = User.objects.get(email=email)
                # The user specified by the email is present, directly add to team
                new_team_member = TeamMember.objects.create(
                    team=team,
                    user=member_user,
                    invitation_full_name=member_user.full_name,
                    invitation_email=member_user.email
                )
            except User.DoesNotExist:
                # The user specified by the email is not present, send invitation
                new_team_member = TeamMember.objects.create(
                    team=team,
                    invitation_full_name=full_name,
                    invitation_email=email
                )
                new_team_member.send_invitation_email()

            response_serializer = TeamMemberSerializer(new_team_member)
            return Response(data=response_serializer.data)


class ConfirmTeamMemberView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request_serializer = ConfirmTeamMemberRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        invitation_token = request_serializer.validated_data['invitation_token']

        try:
            team_member = TeamMember.objects.get(invitation_token=invitation_token)

            # Only allow confirming if the current user's email matches the invitation email
            if team_member.invitation_email == request.user.email:
                team_member.user = request.user
                team_member.invitation_full_name = request.user.full_name
                team_member.save()
            else:
                return Response({
                    'code': 'wrong_email',
                    'detail': 'Please login as the user with the email address to which your invitation email was sent.'
                }, status=status.HTTP_400_BAD_REQUEST)

        except TeamMember.DoesNotExist:
            return Response({
                'code': 'invalid_token',
                'detail': 'The team invitatation token is not valid.'
            }, status=status.HTTP_400_BAD_REQUEST)


class ListTeamsView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # User should only be able to see teams in which he/she is a member
        return Team.objects.filter(team_members__user=self.request.user)


class RetrieveUpdateDestroyTeamView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'team_id'
    serializer_class = TeamDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # User should only be able to see teams in which he/she is a member
        # Disable edit/delete if competition's is_registration_open is false
        if self.request.method == 'GET':
            return self.request.user.teams
        else:
            return self.request.user.teams.filter(competition__is_registration_open=True)


class RetrieveUpdateDestroyTeamMemberView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # User should only be able to see teams in which he/she is a member
        # Disable edit/delete if competition's is_registration_open is false
        if self.request.method == 'GET':
            return TeamMember.objects.filter(team__in=self.request.user.teams)
        else:
            return TeamMember.objects.filter(
                team__in=self.request.user.teams,
                team__competition__is_registration_open=True
            )

    def get_object(self):
        instance = get_object_or_404(
            self.get_queryset(),
            team__id=self.kwargs['team_id'],
            id=self.kwargs['team_member_id'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class SubmitTaskResponseView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, *args, **kwargs):
        # Only team members can submit a response
        team = get_object_or_404(
            Team.objects.all(),
            id=self.kwargs['team_id'],
            team_members__user=self.request.user
        )

        # A team can only respond to tasks in the currently active stage
        task = get_object_or_404(
            Task.objects.all(),
            id=self.kwargs['task_id'],
            stage=team.active_stage,
        )

        request_serializer = TaskResponseSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        response = request_serializer.validated_data['response']

        if team.is_participating:
            # Create or update this TaskResponse, setting its status to awaiting_validation or completed
            # according to the whether this task requires validation,
            # and also updating its last_submitted_at.
            if task.requires_validation:
                task_response_status = TaskResponse.AWAITING_VALIDATION
            else:
                task_response_status = TaskResponse.COMPLETED
            new_task_response = TaskResponse.objects.update_or_create(
                task=task,
                team=team,
                defaults={
                    'response': response,
                    'status': task_response_status,
                    'last_submitted_at': timezone.now(),
                }
            )

            response_serializer = TaskResponseSerializer(new_task_response[0])
            return Response(data=response_serializer.data)
        else:
            return Response({
                'code': 'team_not_participating',
                'detail': 'Your team is no longer participating in this competition.'
            }, status=status.HTTP_400_BAD_REQUEST)
