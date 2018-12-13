from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from arkav_is_api import settings
from arkav_is_api.preevent.models import CodingClassParticipant, Configuration
from arkav_is_api.preevent.serializers import CodingClassRequestSerializer, CodingClassModelSerializer


class RegistrationPing(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        data = {}
        configuration = Configuration.objects.first()
        data['coding_class_registration_open'] = configuration.is_coding_class_registration_open
        return Response(data=data)


class CodingClass(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        obj = CodingClassParticipant.objects.filter(user=request.user).first()
        serialized= CodingClassModelSerializer(obj)

        return Response(data=serialized.data)
    def post(self, request, format=None):
        if not Configuration.objects.first().is_coding_class_registration_open:
            return Response(data={'status': 403, 'message': 'Registration is closed'},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            serialized = CodingClassRequestSerializer(data=request.data)
            if not serialized.is_valid():
                return Response(status=400, data={'status': 400, 'message': serialized.error_messages})
            obj = CodingClassParticipant.objects.filter(user=request.user).first()
            if obj:
                setattr(obj, 'birthday', serialized.validated_data['birthday'])
                setattr(obj, 'domicile', serialized.validated_data['domicile'])
                setattr(obj, 'school', serialized.validated_data['school'])
                setattr(obj, 'grade', serialized.validated_data['grade'])
                obj.save()
            else:
                with transaction.atomic():
                    obj, created = CodingClassParticipant.objects.update_or_create(
                        user=request.user,
                        birthday=serialized.validated_data['birthday'],
                        domicile=serialized.validated_data['domicile'],
                        school=serialized.validated_data['school'],
                        grade=serialized.validated_data['grade'],
                        status=1
                    )
                    obj.add_user_to_quiz_participant()
                    obj.create_user_quiz_attempt()
            return Response(status=200, data={'status': 200, 'message': 'OK'})