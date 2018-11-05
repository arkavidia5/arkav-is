from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    uploaded_by = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = UploadedFile
        fields = ('id', 'original_filename', 'file_size', 'description', 'uploaded_by', 'uploaded_at')
        read_only_fields = ('id', 'original_filename', 'file_size', 'description', 'uploaded_by', 'uploaded_at')
