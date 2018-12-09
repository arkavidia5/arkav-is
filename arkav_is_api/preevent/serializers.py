from rest_framework import serializers

from arkav_is_api.preevent.models import CodingClassParticipant


class CodingClassRequestSerializer(serializers.Serializer):
    birthday = serializers.DateField()
    domicile = serializers.CharField(max_length=100)
    school = serializers.CharField(max_length=150)
    grade = serializers.CharField(max_length=50)
