from rest_framework import serializers
from .models import Competition, Stage, Task, Team, TeamMember, TaskResponse, File, CompetitionCategory

class CompetitionCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionCategory
        fields = ('id','name')
        read_only_fields = ('id','name')
class CompetitionSerializer(serializers.ModelSerializer):
    categories = CompetitionCategoriesSerializer(many=True)
    class Meta:
        model = Competition
        fields = ('id', 'name', 'max_team_members', 'min_team_members', 'is_registration_open', 'categories', 'view_icon')
        read_only_fields = ('id', 'name', 'max_team_members', 'min_team_members', 'is_registration_open', 'categories', 'view_icon')

class TaskSerializer(serializers.ModelSerializer):
    widget = serializers.CharField(source='widget.name')
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Task
        fields = ('id','name', 'category', 'widget', 'widget_parameters')
        read_only_fields = ('id','name', 'category', 'widget', 'widget_parameters')

class StageSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Stage
        fields = ('id', 'name', 'order', 'tasks')
        read_only_fields = ('id', 'name', 'order','tasks')


class TeamMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.full_name', read_only=True)
    id = serializers.IntegerField(source='user.id', read_only=True)
    user_active = serializers.BooleanField(source='user.is_active', read_only=True)
    class Meta:
        model = TeamMember
        fields = ('id', 'email', 'name', 'is_approved', 'created_at', 'user_active')
        read_only_fields = ('id','email', 'name', 'created_at', 'user_active')



class TeamSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    joined_at = serializers.SerializerMethodField()


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
        fields = ('id', 'competition', 'name', 'is_participating', 'team_leader', 'joined_at')
        read_only_fields = ('id', 'competition', 'is_participating', 'team_leader', 'joined_at')


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
            'id', 'competition', 'name', 'secret_code', 'is_participating', 'created_at',
            'team_members', 'active_stage_id', 'stages', 'task_responses', 'team_leader'
        )
        read_only_fields = (
            'id', 'competition', 'secret_code', 'is_participating', 'created_at',
            'team_members', 'active_stage_id', 'stages', 'task_responses'
        )

class RegisterTeamMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
class RegisterTeamRequestSerializer(serializers.Serializer):
    competition_id = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all())
    team_name = serializers.CharField(max_length=50, min_length=3)
    team_category = serializers.CharField(max_length=50)
    team_school = serializers.CharField(max_length=30)
    members = RegisterTeamMemberRequestSerializer(many=True)


class JoinTeamRequestSerializer(serializers.Serializer):
    secret_code = serializers.CharField()


# TODO: move to separate app/package
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'slug')

