import re

from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from arkav_is_api import settings
from arkav_is_api.seminar.models import Configuration, Registrant, Ticket


def issue_ticket(model, request, queryset):
    for item in queryset:
        if item.is_valid:
            print(item.user)
            item.issue_ticket()
        else:
            print(item.user, "not valid")


issue_ticket.short_description = "Issue Ticket for all Registrant"

def send_reminder(model, request, queryset):
    for item in queryset:
        if item.status == 0 and not item.is_valid:
            # print(item.user)
            item.send_reminder()




@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['is_registration_open', 'session_one_normal_price', 'session_two_price',
                    'session_one_max_capacity',
                    'session_two_max_capacity', 'session_one_current_capacity',
                    'session_two_current_capacity']
    pass

@admin.register(Registrant)
class RegistrationAdmin(admin.ModelAdmin):
    actions = [issue_ticket, send_reminder]
    list_display = ['user', 'status', 'is_register_session_one', 'is_register_session_two',
                    'is_valid','payment_receipt', 'created_at', 'updated_at']
    readonly_fields = ['user_name', 'payment_receipt_link','payment_receipt_file', 'created_at', 'updated_at']
    def user_name(self,instance):
        return instance.user.full_name
    def payment_receipt_link(self, instance):
        uuidv4_regex = r'[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}'
        if re.match(uuidv4_regex, str(instance.payment_receipt)) is not None:
            link = reverse('download', kwargs={'file_id': str(instance.payment_receipt)})
            return 'http://dashboard.arkavidia.id'+link
        else:
            return ''
    def payment_receipt_file(self, instance):
        uuidv4_regex = r'[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}'
        if re.match(uuidv4_regex, str(instance.payment_receipt)) is not None:
            link = reverse('download', kwargs={'file_id': str(instance.payment_receipt)})
            return format_html('<a href="{}">Open file</a>', link)
        else:
            return ''
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['registrant_name', 'booking_number']
    def registrant_name(self, instance):
        return instance.registrant.user