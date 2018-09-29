from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from string import ascii_uppercase, ascii_lowercase, digits, ascii_letters


def generate_random_str(length=30):
    return get_random_string(length, allowed_chars=ascii_letters)


def generate_team_secret_code():
    """
    Generate a new random secret code for identifying a team (for team member registrations).
    Format: 6 characters, uppercase alphabet and numbers.
    """
    return get_random_string(length=6, allowed_chars=ascii_uppercase+digits)


class Competition(models.Model):
    name = models.CharField(max_length=50)
    max_team_members = models.IntegerField(default=1)
    is_registration_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    """
    A competition contains one or more stages, e.g. registration, qualification and final stages.
    The ordering of stages is specified manually as an integer, with respect to competition.
    """
    competition = models.ForeignKey(to=Competition, related_name='stages', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.competition.name, self.name)

    class Meta:
        ordering = ['competition', 'order']


class TaskCategory(models.Model):
    """
    The category label for this task, e.g. payment, proposal upload, etc.
    Used to help staff filter relevant tasks.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'task categories'


class TaskWidget(models.Model):
    """
    The type of widget (component) to be shown to the user for completing this task,
    e.g. text_input, file_upload.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    A stage contains one or more tasks, e.g. payment, upload proposal, etc.
    """
    stage = models.ForeignKey(to=Stage, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(to=TaskCategory, related_name='tasks', on_delete=models.PROTECT)
    widget = models.ForeignKey(to=TaskWidget, related_name='tasks', on_delete=models.PROTECT)
    widget_parameters = models.TextField()
    requires_validation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    """
    A competition can have participating teams.
    - A team can only see stages up to the active_stage;
      stages which comes after the active_stage are not visible.
    - A team can only respond to tasks in the currently active stage
      and only if is_participating is True; all other stages are locked.
    - active_stage defaults to the first stage in the team's competition;
      creation fails if the team's competition does not have a stage yet.
    """
    competition = models.ForeignKey(to=Competition, related_name='teams', on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    secret_code = models.CharField(max_length=20, default=generate_team_secret_code, unique=True)
    members = models.ManyToManyField(to=User, related_name='teams', through='TeamMember')
    active_stage = models.ForeignKey(to=Stage, related_name='active_teams', on_delete=models.PROTECT)
    is_participating = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def approved_members(self):
        return User.objects.filter(team_members__team=self, team_members__is_approved=True)

    @property
    def pending_members(self):
        return User.objects.filter(team_members__team=self, team_members__is_approved=False)

    @property
    def has_completed_active_stage(self):
        active_stage_task_count = self.active_stage.tasks.count()
        active_stage_completed_task_count = self.task_responses.filter(
            task__stage=self.active_stage, status=TaskResponse.COMPLETED).count()
        return active_stage_task_count == active_stage_completed_task_count

    def generate_secret_code(self):
        return generate_team_secret_code()

    def save(self, *args, **kwargs):
        # Use the first stage of the competition as the default for active_stage.
        # Will fail if no competition is set or the competition does not have a stage yet.
        if self.pk is None and not hasattr(self, 'active_stage'):
            try:
                competition_first_stage = self.competition.stages.first()
            except AttributeError as e:
                raise ValueError('Team must have a competition set.') from e
            if competition_first_stage is None:
                raise ValueError('Team must have a competition with at least 1 stage.')
            self.active_stage = competition_first_stage

        super(Team, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = 'created_at'


class TeamMember(models.Model):
    """
    Many-to-many through/pivot table between Team and User.
    """
    team = models.ForeignKey(to=Team, related_name='team_members', on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, related_name='team_members', on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.team.name, self.user.username)

    class Meta:
        unique_together = (('team', 'user'),)  # Each team-user pair must be unique
        get_latest_by = 'created_at'


class TaskResponse(models.Model):
    """
    A response to a task, e.g. proof of payment image, uploaded proposal.
    A TaskResponse will be created when a response is submitted for a task.
    Each team can only have at most 1 task response per task;
    resubmissions will update the existing TaskResponse and reset its state to awaiting_validation.
    """
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

    def save(self, *args, **kwargs):
        # If this response's task's requires_validation is True,
        # use awaiting_validation as the default state, else use completed.
        if self.pk is None and (self.status is None or self.status == ''):
            if self.task.requires_validation:
                self.status = self.AWAITING_VALIDATION
            else:
                self.status = self.COMPLETED

        super(TaskResponse, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('task', 'team'),)  # Each team can only have at most 1 task response per task
        get_latest_by = 'created_at'


class File(models.Model):
    slug = models.CharField(default=generate_random_str, max_length=30)
    filename = models.CharField(max_length=30)
