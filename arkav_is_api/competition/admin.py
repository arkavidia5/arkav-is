from django.contrib import admin
from .models import (
    Competition,
    Stage,
    Task,
    Team,
    TeamMember,
    TaskResponse,
)


class StageInline(admin.TabularInline):
    model = Stage
    fields = ['name']
    extra = 1
    show_change_link = True


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'max_team_members', 'is_registration_open']
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
    list_display = ['id', 'name', 'competition']
    list_display_links = ['id', 'name']
    list_filter = ['competition']
    search_fields = ['name']
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stage', 'category', 'widget', 'requires_validation']
    list_display_links = ['id', 'name']
    list_filter = ['stage__competition', 'category', 'widget']
    search_fields = ['name']


@admin.register(TaskResponse)
class TaskResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'task', 'status', 'created_at']
    list_display_links = ['id']
    list_filter = ['status', 'task__category']
    search_fields = ['team', 'task']
    autocomplete_fields = ['team', 'task']


class TaskResponseInline(admin.TabularInline):
    model = TaskResponse
    fields = ['team', 'task', 'status', 'response', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ['team', 'task']
    extra = 1


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    fields = ['user', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ['user']
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'competition', 'active_stage', 'is_participating', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['competition', 'is_participating']
    search_fields = ['name']
    inlines = [TeamMemberInline, TaskResponseInline]
