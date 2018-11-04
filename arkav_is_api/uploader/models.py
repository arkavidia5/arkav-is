import os
from django.db import models
from arkav_is_api.arkavauth.models import User


def generate_upload_to_path(instance, filename):
    if instance.id is None:
        raise RuntimeError('Uploaded file ID has not been set.')
    return os.path.join('uploads/', str(instance.id))


class UploadedFile(models.Model):
    file = models.FileField(upload_to=generate_upload_to_path)
    id = models.UUIDField(primary_key=True, editable=False)
    original_filename = models.CharField(max_length=200)
    file_size = models.BigIntegerField()
    description = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(to=User, related_name='uploaded_files', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename
