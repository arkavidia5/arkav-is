from rest_framework import serializers
from .models import Competition, Stage, Team, TeamMember, TaskResponse, File


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'max_team_members', 'min_team_members', 'is_registration_open', 'view_icon')
        read_only_fields = ('id', 'name', 'max_team_members', 'min_team_members', 'is_registration_open', 'view_icon')


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('id', 'name', 'order')
        read_only_fields = ('id', 'name', 'order')


class TeamSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    is_approved_team_member = serializers.SerializerMethodField()
    joined_at = serializers.SerializerMethodField()

    def get_is_approved_team_member(self, instance):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            try:
                return TeamMember.objects.get(team=instance, user=current_user).is_approved
            except TeamMember.DoesNotExist:
                return False
        else:
            return False

    def get_joined_at(self, instance):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            try:
                return TeamMember.objects.get(team=instance, user=current_user).created_at
            except TeamMember.DoesNotExist:
                return None
        else:
            return None

    class Meta:
        model = Team
        fields = ('id', 'competition', 'name', 'is_participating', 'is_approved_team_member', 'joined_at', 'team_leader')
        read_only_fields = ('id', 'competition', 'is_participating', 'is_approved_team_member', 'joined_at', 'team_leader')


class TeamMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = TeamMember
        fields = ('username', 'name', 'is_approved', 'created_at')
        read_only_fields = ('username', 'name', 'created_at')


class TaskResponseSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(source='task', read_only=True)

    class Meta:
        model = TaskResponse
        fields = ('task_id', 'response', 'status', 'last_submitted_at')
        read_only_fields = ('task_id', 'status', 'last_submitted_at')


class TeamDetailsSerializer(TeamSerializer):
    competition = CompetitionSerializer(read_only=True)
    team_members = TeamMemberSerializer(many=True, read_only=True)
    active_stage_id = serializers.PrimaryKeyRelatedField(source='active_stage', read_only=True)
    stages = StageSerializer(source='visible_stages', many=True, read_only=True)
    task_responses = TaskResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            'id', 'competition', 'name', 'secret_code', 'is_participating', 'joined_at', 'created_at',
            'team_members', 'active_stage_id', 'stages', 'task_responses', 'team_leader'
        )
        read_only_fields = (
            'id', 'competition', 'secret_code', 'is_participating', 'joined_at', 'created_at',
            'team_members', 'active_stage_id', 'stages', 'task_responses'
        )


class RegisterTeamRequestSerializer(serializers.Serializer):
    competition_id = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all())
    team_name = serializers.CharField(max_length=50, min_length=3)


class JoinTeamRequestSerializer(serializers.Serializer):
    secret_code = serializers.CharField()


# TODO: move to separate app/package
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'slug')
