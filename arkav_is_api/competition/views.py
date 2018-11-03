import boto3
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# TODO: fix to use proper Django setting import
from arkav_is_api.settings import S3_BUCKET_BASE_URL, UPLOAD_DIR, S3_BUCKET_NAME

from .models import (
    Competition,
    Team,
    TeamMember,
    Task,
    TaskResponse,
    File,
)
from .serializers import (
    CompetitionSerializer,
    RegisterTeamRequestSerializer,
    JoinTeamRequestSerializer,
    TeamSerializer,
    TeamDetailsSerializer,
    TeamMemberSerializer,
    TaskResponseSerializer,
    FileSerializer,
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
        team_name = request_serializer.validated_data['team_name']

        # Only register if registration is open for this competition
        if competition.is_registration_open:
            with transaction.atomic():
                # A user can't register in a competition if he/she already participated in the same competition
                if TeamMember.objects.filter(team__competition=competition, user=request.user).exists():
                    raise ValidationError(
                        code='competition_already_registered',
                        detail='You can only participate in one team per competition.',
                    )

                # Create a new team and add the current user as an approved member to the team
                new_team = Team.objects.create(competition=competition, name=team_name)
                TeamMember.objects.create(team=new_team, user=request.user, is_approved=True)

                response_serializer = TeamSerializer(new_team)
                return Response(data=response_serializer.data)
        else:
            raise ValidationError(
                code='competition_registration_closed',
                detail='The competition you are trying to register to is not open for registration.',
            )


class JoinTeamView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request_serializer = JoinTeamRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        try:
            team = Team.objects.select_related('competition', 'members').get(
                secret_code=request_serializer.validated_data['secret_code'],
            )
        except Team.DoesNotExist:
            raise ValidationError(
                code='invalid_secret_code',
                detail='The team invitation code you entered is not valid.',
            )

        # Only allow new team member if registration is open for the team's competition,
        # and the number of team members is still less than the maximum team members limit.
        if team.competition.is_registration_open and team.members.count() < team.competition.max_team_members:
            with transaction.atomic():
                # A user can't register in a competition if he/she already participated in the same competition
                if TeamMember.objects.filter(team__competition=team.competition, user=request.user).exists():
                    raise ValidationError(
                        code='competition_already_registered',
                        detail='You can only participate in one team per competition.',
                    )

                # Add the current user to the team (pending approval)
                TeamMember.objects.create(team=team, user=request.user)

                response_serializer = TeamSerializer(team)
                return Response(data=response_serializer.data)
        else:
            raise ValidationError(
                code='competition_registration_closed',
                detail='The competition you are trying to register to is not open for registration.',
            )


class ListTeamsView(generics.ListAPIView):
        serializer_class = TeamSerializer
        permission_classes = (IsAuthenticated,)
        def get_queryset(self):
            return Team.objects.filter(team_members__user__email__in=[self.request.user])


class RetrieveUpdateTeamView(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = 'team_id'
    serializer_class = TeamDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # User should only be able to see teams which he/she has been approved as a member
        return Team.objects.filter(
            team_members__user=self.request.user,
            team_members__is_approved=True,
        )


# TODO: disable delete if competition's is_registration_open is false
class RetrieveUpdateDestroyTeamMemberView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # User should only be able to see teams which he/she has been approved as a member,
        # except for deleting, for which the user can delete teams in which he/she is still pending confirmation.
        if self.request.method == 'DELETE':
            return TeamMember.objects.filter(user=self.request.user)
        else:
            return TeamMember.objects.filter(user=self.request.user, is_approved=True)

    def get_object(self):
        instance = get_object_or_404(
            self.get_queryset(),
            team__id=self.kwargs['team_id'],
            user__username=self.kwargs['username'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class SubmitTaskResponseView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # Only approved team members can submit a response
        team = get_object_or_404(
            Team.objects.all(),
            id=self.kwargs['team_id'],
            team_members__user=self.request.user,
            team_members__is_approved=True,
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
                },
            )

            response_serializer = TaskResponseSerializer(new_task_response)
            return Response(data=response_serializer.data)
        else:
            raise ValidationError(
                code='team_not_participating',
                detail='Your team is no longer participating in this competition.',
            )


# TODO: move to separate app/package
class FileView(views.APIView):
    """
    Get file URL or upload a file
    """
    renderer_classes = (JSONRenderer,)

    def get(self, request, slug=None, format=None):
        try:
            File.objects.get(slug=slug)
        except File.DoesNotExist:
            data = {
                "error": "File Not Found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data = {
            "url": f"{S3_BUCKET_BASE_URL}/{slug}"
        }

        return Response(data)

    def post(self, request, slug=None, format=None):
        uploaded_file = request.data['file']
        filename = request.data['filename']
        with open(f'{UPLOAD_DIR}/{filename}', 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        file = File(filename=filename)
        file.save()

        # self.upload_to_s3(filename, file.slug)
        data = FileSerializer(file).data

        return Response(data)

    def upload_to_s3(self, filename, slug):
        s3 = boto3.client("s3")
        s3.upload_file(f"{UPLOAD_DIR}/{filename}", S3_BUCKET_NAME, slug)
