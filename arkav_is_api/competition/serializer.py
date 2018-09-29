from rest_framework import serializers
from arkav_is_api.competition.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'slug')