import uuid
from django import forms
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import UploadedFile

# TODO: add per-user upload size quota


class UploadFileForm(forms.Form):
    file = forms.FileField()
    description = forms.CharField(max_length=200, required=False)


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
            content_type=form.cleaned_data['file'].content_type,
            description=form.cleaned_data['description'],
        )
        instance.file = form.cleaned_data['file']
        instance.save()
        return JsonResponse(
            {
                'id': instance.id,
                'original_filename': instance.original_filename,
                'file_size': instance.file_size,
                'content_type': instance.content_type,
                'uploaded_by': instance.uploaded_by.email,
                'uploaded_at': instance.uploaded_at,
                'description': instance.description,
            },
            status=201,
        )
    else:
        print(form.errors)
        return JsonResponse(
            {
                'errors': form.errors,
            },
            status=400,
        )


@login_required
@require_GET
def download_file_view(request, file_id):
    """
    Download an uploaded file with the matching file_id.
    file_id is a UUIDv4, which is hard to guess, so it should be quite secure
    as long all pages which contain a link to it requires login.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    response = HttpResponse(uploaded_file.file.open('rb'), content_type = uploaded_file.content_type )
    # response['Content-Type'] = 'application/pdf'
    # response['Content-Disposition'] = 'inline; filename=' + uploaded_file.original_filename
    return response
