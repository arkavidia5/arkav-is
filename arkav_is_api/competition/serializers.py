from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from arkav_is_api.arkavauth.models import User
from .models import Competition, Stage, Task, Team, TeamMember, TaskResponse, CompetitionCategory


class CompetitionSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Competition
        fields = (
            'id', 'name', 'max_team_members', 'min_team_members', 'is_registration_open',
            'categories', 'view_icon'
        )
        read_only_fields = (
            'id', 'name', 'max_team_members', 'min_team_members', 'is_registration_open',
            'categories', 'view_icon'
        )


class TaskSerializer(serializers.ModelSerializer):
    widget = serializers.CharField(source='widget.name')
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Task
        fields = ('id', 'name', 'category', 'widget', 'widget_parameters')
        read_only_fields = ('id', 'name', 'category', 'widget', 'widget_parameters')


class StageSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Stage
        fields = ('id', 'name', 'order', 'tasks')
        read_only_fields = ('id', 'name', 'order', 'tasks')


class TeamMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = TeamMember
        fields = (
            'full_name', 'email', 'has_account', 'invitation_token', 'email_last_sent_at', 'created_at'
        )
        read_only_fields = (
            'full_name', 'email', 'has_account', 'invitation_token', 'email_last_sent_at', 'created_at'
        )


class TaskResponseSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(source='task', read_only=True)

    class Meta:
        model = TaskResponse
        fields = ('task_id', 'response', 'status', 'last_submitted_at')
        read_only_fields = ('task_id', 'status', 'last_submitted_at')


class TeamSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    team_leader_email = serializers.SlugRelatedField(source='team_leader', slug_field='email', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'competition', 'name', 'team_leader_email', 'institution',
                  'is_participating', 'category')
        read_only_fields = ('id', 'competition', 'name', 'team_leader_email', 'institution',
                            'is_participating', 'category')


class TeamDetailsSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    team_leader_email = serializers.SlugRelatedField(source='team_leader', slug_field='email',
                                                     queryset=User.objects.all())
    team_members = TeamMemberSerializer(many=True, read_only=True)
    active_stage_id = serializers.PrimaryKeyRelatedField(source='active_stage', read_only=True)
    stages = StageSerializer(source='visible_stages', many=True, read_only=True)
    task_responses = TaskResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            'id', 'competition', 'category', 'name', 'team_leader_email', 'institution',
            'is_participating', 'team_members', 'active_stage_id', 'stages', 'task_responses',
            'created_at'
        )
        read_only_fields = (
            'id', 'competition', 'category', 'is_participating', 'team_members',
            'active_stage_id', 'stages', 'task_responses', 'created_at'
        )


class RegisterTeamRequestSerializer(serializers.Serializer):
    competition_id = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all())
    name = serializers.CharField(max_length=50, min_length=3, validators=[UniqueValidator(queryset=Team.objects.all())])
    category = serializers.SlugRelatedField(slug_field='name', queryset=CompetitionCategory.objects.all())
    institution = serializers.CharField(max_length=50)


class AddTeamMemberRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=75)
    email = serializers.EmailField()


class ConfirmTeamMemberRequestSerializer(serializers.Serializer):
    invitation_token = serializers.CharField()
