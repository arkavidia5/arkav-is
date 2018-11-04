import uuid
from django import forms
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import UploadedFile

# TODO: add per-user upload size quota


class UploadFileForm(forms.Form):
    file = forms.FileField()
    description = forms.CharField(max_length=200)


@login_required
@require_POST
def upload_file_view(request):
    """
    Handle file upload (Django request, not using DRF).
    """
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        instance = UploadedFile(
            id=uuid.uuid4(),
            original_filename=form.cleaned_data['file'].name,
            file_size=form.cleaned_data['file'].size,
            uploaded_by=request.user,
            description=form.cleaned_data['description'],
        )
        instance.file = form.cleaned_data['file']
        instance.save()
        return JsonResponse(
            {
                'id': instance.id,
                'original_filename': instance.original_filename,
                'file_size': instance.file_size,
                'uploaded_by': instance.uploaded_by.email,
                'uploaded_at': instance.uploaded_at,
                'description': instance.description,
            },
            status=201,
        )
    else:
        return JsonResponse(
            {
                'errors': form.errors,
            },
            status=400,
        )
