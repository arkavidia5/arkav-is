from django.contrib import admin
from .models import (
    Competition,
    Stage,
    Task,
    Team,
    TeamMember,
    TaskResponse,
    CompetitionCategory,
    TaskCategory,
    TaskWidget,
)


class StageInline(admin.TabularInline):
    model = Stage
    fields = ['name', 'order']
    extra = 1
    show_change_link = True


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'min_team_members','max_team_members', 'is_registration_open']
    list_display_links = ['id', 'name']
    list_filter = ['is_registration_open']
    inlines = [StageInline]


class TaskInline(admin.TabularInline):
    model = Task
    fields = ['name', 'stage', 'category', 'widget', 'requires_validation']
    extra = 1
    show_change_link = True


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'competition', 'order']
    list_display_links = ['id', 'name']
    list_filter = ['competition']
    search_fields = ['name']
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stage', 'category', 'widget', 'requires_validation']
    list_display_links = ['id', 'name']
    list_filter = ['category', 'widget', 'stage__competition', 'stage']
    search_fields = ['name']


@admin.register(TaskResponse)
class TaskResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'task', 'status', 'last_submitted_at']
    list_display_links = ['id']
    list_filter = ['status', 'task__category']
    search_fields = ['team', 'task']
    autocomplete_fields = ['team', 'task']


class TaskResponseInline(admin.TabularInline):
    model = TaskResponse
    fields = ['team', 'task', 'status', 'response', 'last_submitted_at']
    readonly_fields = ['last_submitted_at']
    autocomplete_fields = ['team', 'task']
    extra = 1


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    fields = ['user', 'is_approved', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ['user']
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'competition', 'active_stage', 'has_completed_active_stage',
                    'is_participating', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_participating', 'competition', 'active_stage']
    search_fields = ['name']
    inlines = [TeamMemberInline, TaskResponseInline]

    # Tell Django that this method returns a boolean value
    def has_completed_active_stage(self, instance):
        return instance.has_completed_active_stage
    has_completed_active_stage.boolean = True

@admin.register(CompetitionCategory)
class CompetitionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']

@admin.register(TaskWidget)
class TaskWidgetAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
