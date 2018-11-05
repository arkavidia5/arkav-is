from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import UploadedFile


@admin.register(UploadedFile)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['file_link', 'id', 'original_filename', 'file_size', 'uploaded_by', 'uploaded_at']
    list_display_links = ['id', 'original_filename']
    search_fields = ['original_filename', 'uploaded_by']
    readonly_fields = ['file_link', 'id', 'file_size']
    autocomplete_fields = ['uploaded_by']

    def file_link(self, instance):
        link = reverse('download', kwargs={'file_id': str(instance.id)})
        return format_html('<a href="{}" download="{}">Download</a>', link, instance.original_filename)

    class Meta:
        ordering = ['-uploaded_at']
