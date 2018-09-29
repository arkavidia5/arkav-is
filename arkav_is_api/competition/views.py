import boto3
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from arkav_is_api.competition.models import File
from arkav_is_api.settings import S3_BUCKET_BASE_URL, UPLOAD_DIR, S3_BUCKET_NAME
from arkav_is_api.competition.serializer import FileSerializer

# Create your views here.

# TODO: task responses state machine

# TODO: Check whether competition's is_registration_open is True when creating the team.

# TODO: auth and permissions

# TODO: tests


class FileView(APIView):
    """
    Get file URL or upload a file
    """
    renderer_classes = (JSONRenderer,)

    def get(self, request, slug=None, format=None):
        try:
            _ = File.objects.get(slug=slug)
        except File.DoesNotExist:
            data = {
                "error": "File Not Found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data = {
            "url": f"{S3_BUCKET_BASE_URL}/{slug}"
        }

        return Response(data)

    def post(self, request, slug=None, format=None):
        uploaded_file = request.data['file']
        filename = request.data['filename']
        with open(f'{UPLOAD_DIR}/{filename}', 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        file = File(filename=filename)
        file.save()

        # self.upload_to_s3(filename, file.slug)
        data = FileSerializer(file).data

        return Response(data)

    def upload_to_s3(self, filename, slug):
        s3 = boto3.client("s3")
        s3.upload_file(f"{UPLOAD_DIR}/{filename}", S3_BUCKET_NAME, slug)

