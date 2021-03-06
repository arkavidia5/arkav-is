from rest_framework import serializers

from arkav_is_api.preevent.models import CodingClassParticipant

class CodingClassModelSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = CodingClassParticipant
        fields = ('birthday', 'school', 'domicile', 'grade','student_card', 'status', 'status_display')



class CodingClassRequestSerializer(serializers.Serializer):
    birthday = serializers.DateField()
    domicile = serializers.CharField(max_length=100)
    school = serializers.CharField(max_length=150)
    grade = serializers.CharField(max_length=50)
    student_card = serializers.CharField(max_length=100)
