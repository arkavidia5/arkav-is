from rest_framework import serializers

from arkav_is_api.seminar.models import Configuration, Registrant


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Configuration
        fields = '__all__'
class RegistrantSerializer(serializers.ModelSerializer):
    class Meta:
        model= Registrant
        fields= '__all__'
class SeminarRegistrationRequestSerializer(serializers.Serializer):
    is_register_session_one = serializers.BooleanField()
    is_register_session_two = serializers.BooleanField()

class PaymentReceiptRequestSerializer(serializers.Serializer):
    payment_receipt = serializers.UUIDField()