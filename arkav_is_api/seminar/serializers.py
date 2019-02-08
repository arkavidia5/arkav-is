from rest_framework import serializers

from arkav_is_api.arkavauth.serializers import UserSerializer
from arkav_is_api.seminar.models import Configuration, Registrant, Ticket



class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Configuration
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields= '__all__'

class RegistrantSerializer(serializers.ModelSerializer):
    ticket= TicketSerializer(many=False)
    class Meta:
        model= Registrant
        fields= '__all__'
class SeminarRegistrationRequestSerializer(serializers.Serializer):
    is_register_session_one = serializers.BooleanField()
    is_register_session_two = serializers.BooleanField()

class GateRequestSerializer(serializers.Serializer):
    session = serializers.IntegerField()
    booking_number = serializers.CharField(max_length=10)

class PaymentReceiptRequestSerializer(serializers.Serializer):
    payment_receipt = serializers.UUIDField()
