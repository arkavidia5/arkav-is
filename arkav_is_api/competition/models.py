from django.db import models
from django.contrib.auth.models import User


# TODO: auth and permissions
# TODO: tests

class Competition(models.Model):
    name = models.CharField(max_length=50)
    max_team_members = models.IntegerField(default=1)
    is_registration_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    '''
    A competition contains one or more stages, e.g. registration, qualification and final stages.
    The ordering of stages is specified with respect to competition.
    '''
    competition = models.ForeignKey(to=Competition, related_name='stages', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s - %s' % (self.competition.name, self.name)

    class Meta:
        order_with_respect_to = 'competition'


class TaskCategory(models.Model):
    '''
    The category label for this task, e.g. payment, proposal upload, etc.
    Used to help staff filter relevant tasks.
    '''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'task categories'


class TaskWidget(models.Model):
    '''
    The type of widget (component) to be shown to the user for completing this task,
    e.g. text_input, file_upload.
    '''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    '''
    A stage contains one or more tasks, e.g. payment, upload proposal, etc.
    '''
    stage = models.ForeignKey(to=Stage, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(to=TaskCategory, related_name='tasks', on_delete=models.PROTECT)
    widget = models.ForeignKey(to=TaskWidget, related_name='tasks', on_delete=models.PROTECT)
    widget_parameters = models.TextField()
    requires_validation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    '''
    A competition can have participating teams.
    - A team can only see stages up to the active_stage;
      stages which comes after the active_stage are not visible.
    - A team can only respond to tasks in the currently active stage
      and only if is_participating is True; all other stages are locked.
    - active_stage defaults to the first stage in the team's competition;
      creation fails if the team's competition does not have a stage yet.
    '''
    competition = models.ForeignKey(to=Competition, related_name='teams', on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    secret_code = models.CharField(max_length=20, unique=True)  # To be used for joining this team
    members = models.ManyToManyField(to=User, related_name='teams', through='TeamMember')
    active_stage = models.ForeignKey(to=Stage, related_name='active_teams', on_delete=models.PROTECT)
    is_participating = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # TODO: implement secret_code and active_stage defaults
    # TODO: check whether competition's is_registration_open is True when registering

    class Meta:
        get_latest_by = 'created_at'


class TeamMember(models.Model):
    '''
    Many-to-many through/pivot table between Team and User.
    '''
    team = models.ForeignKey(to=Team, related_name='team_members', on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, related_name='team_members', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.team.name, self.user.username)

    class Meta:
        unique_together = (('team', 'user'),)  # Each team-user pair must be unique
        get_latest_by = 'created_at'


class TaskResponse(models.Model):
    '''
    A response to a task, e.g. proof of payment image, uploaded proposal.
    A TaskResponse will be created when a response is submitted for a task.
    Each team can only have at most 1 task response per task;
    resubmissions will update the existing TaskResponse and reset its state to awaiting_validation.
    '''
    AWAITING_VALIDATION = 'awaiting_validation'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (AWAITING_VALIDATION, 'Awaiting validation'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
    )

    task = models.ForeignKey(to=Task, related_name='task_responses', on_delete=models.PROTECT)
    team = models.ForeignKey(to=Team, related_name='task_responses', on_delete=models.PROTECT)
    response = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.task.name, self.team.name)

    # TODO: implement status change state machine

    class Meta:
        unique_together = (('task', 'team'),)  # Each team can only have at most 1 task response per task
        get_latest_by = 'created_at'
