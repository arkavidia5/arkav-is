import re

from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from arkav_is_api.seminar.models import Configuration, Registrant


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['is_registration_open', 'session_one_normal_price', 'session_two_price',
                    'session_one_max_capacity',
                    'session_two_max_capacity', 'session_one_current_capacity',
                    'session_two_current_capacity']
    pass

@admin.register(Registrant)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'is_register_session_one', 'is_register_session_two', 'payment_receipt', 'created_at', 'updated_at']
    readonly_fields = ['payment_receipt_file', 'created_at', 'updated_at']

    def payment_receipt_file(self, instance):
        uuidv4_regex = r'[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}'
        if re.match(uuidv4_regex, str(instance.payment_receipt)) is not None:
            link = reverse('download', kwargs={'file_id': str(instance.payment_receipt)})
            return format_html('<a href="{}">Open file</a>', link)
        else:
            return ''

    pass
