from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_filename', 'file_size', 'uploaded_by', 'uploaded_at']
    list_display_links = ['id', 'original_filename']
    search_fields = ['original_filename', 'uploaded_by']
    readonly_fields = ['id', 'file_size']
    autocomplete_fields = ['uploaded_by']

    class Meta:
        ordering = ['-uploaded_at']
