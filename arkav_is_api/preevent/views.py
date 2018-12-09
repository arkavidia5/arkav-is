from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from arkav_is_api import settings
from arkav_is_api.preevent.models import CodingClassParticipant
from arkav_is_api.preevent.serializers import CodingClassRequestSerializer


class CodingClass(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        data= {}
        data['is_registration_open'] = settings.CODING_CLASS_REGISTRATION_OPEN
        return Response(data=data)
    def post(self, request, format=None):
        if not settings.CODING_CLASS_REGISTRATION_OPEN:
            return Response(data={'status': 403, 'message': 'Registration is closed'},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            serialized = CodingClassRequestSerializer(data=request.data)
            if not serialized.is_valid():
                return Response(status=400, data={'status': 400, 'message': serialized.error_messages})
            if CodingClassParticipant.objects.filter(user=request.user).first():
                return Response(status=403, data={'status': 403, 'message': 'Satu user hanya dapat mendaftar sekali'})

            with transaction.atomic():
                obj = CodingClassParticipant.objects.create(
                    user= request.user,
                    birthday= serialized.validated_data['birthday'],
                    domicile= serialized.validated_data['domicile'],
                    school= serialized.validated_data['school'],
                    grade= serialized.validated_data['grade'],
                    status= 1
                )
                obj.add_user_to_quiz_participant()
                obj.create_user_quiz_attempt()
                return Response(status=200, data={'status': 200, 'message': 'OK'})