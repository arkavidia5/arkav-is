from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from arkav_is_api.seminar.models import Configuration, Registrant
from arkav_is_api.seminar.serializers import SeminarRegistrationRequestSerializer, ConfigurationSerializer, \
    RegistrantSerializer, PaymentReceiptRequestSerializer


class SeminarPing(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        data = {}
        configuration = Configuration.objects.first()
        data['is_registration_open'] = configuration.is_registration_open
        return Response(data=data)
class SeminarConfiguration(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        configuration = Configuration.objects.first()
        serialized = ConfigurationSerializer(configuration).data
        return Response(data=serialized)

class PaymentReceipt(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serialized = PaymentReceiptRequestSerializer(data=request.data)
        if(serialized.is_valid()):
            with transaction.atomic():
                registrant = Registrant.objects.filter(user=request.user).first()
                registrant.payment_receipt= serialized.validated_data['payment_receipt']
                registrant.status = 1
                registrant.save()
                return Response(status=200)
        else:
            return Response(status=400)

class RegisterView(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(selfs, request, format=None):
        registration_data = Registrant.objects.filter(user=request.user)
        if(registration_data.count() > 0):
            return Response(data=RegistrantSerializer(registration_data.first()).data)
        else:
            return Response(data=None)


    def post(self, request, format=None):
        serialized = SeminarRegistrationRequestSerializer(data= request.data)
        config = Configuration.objects.first()
        instance = Registrant.objects.filter(user=request.user)
        if serialized.is_valid():
            try:
                with transaction.atomic():

                    if(instance.count() == 0):
                        if (serialized.validated_data['is_register_session_one']):
                            config.reserve_session_one()
                        if (serialized.validated_data['is_register_session_two']):
                            config.reserve_session_two()
                        Registrant.objects.create_or_update(
                            user= request.user,
                            is_register_session_one= serialized.validated_data['is_register_session_one'],
                            is_register_session_two= serialized.validated_data['is_register_session_two']
                        )
                    else:
                        instance = instance.first()
                        if(instance.is_register_session_one):
                            config.unreserve_session_one()
                        if(instance.is_register_session_two):
                            config.unreserve_session_two()
                        if (serialized.validated_data['is_register_session_one']):
                            config.reserve_session_one()
                        if (serialized.validated_data['is_register_session_two']):
                            config.reserve_session_two()
                        instance.is_register_session_one = serialized.validated_data['is_register_session_one']
                        instance.is_register_session_two = serialized.validated_data['is_register_session_two']
                        instance.save()
                    return Response(status=200)
            except Exception as err:
                return Response(status=400, data=err.args[0])
