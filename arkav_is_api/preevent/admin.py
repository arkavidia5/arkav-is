from django.contrib import admin
import re
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from arkav_is_api.preevent.models import CodingClassParticipant, Configuration

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        'singleton','is_coding_class_registration_open', 'coding_class_quiz_slug'
    )
    def singleton(self,obj):
        return 'Preevent Configuration '
    pass


def add_user_attempt(model, request, queryset):
    for item in queryset:
        item.add_user_to_quiz_participant()
        item.create_user_quiz_attempt()

add_user_attempt.short_description = 'Create user quiz attempt'

def finish_user_quiz(model, request, queryset):
    for item in queryset:
        item.finish_quiz()

finish_user_quiz.short_desciption = 'finish user quiz'

@admin.register(CodingClassParticipant)
class CodingClassParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "user", "user_name", "domicile","school" , "grade", "quiz_attempt", "quiz_attempt_score", "status"
    ]
    actions =  [
        add_user_attempt,
        finish_user_quiz
    ]
    readonly_fields = ('user_name','quiz_attempt_score', 'file_link')

    def file_link(self, instance):
        uuidv4_regex = r'[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}'
        if re.match(uuidv4_regex, str(instance.student_card)) is not None:
            link = reverse('download', kwargs={'file_id': str(instance.student_card)})
            return format_html('<a href="{}">Open file</a>', link)
        else:
            return ''

    def user_name(self,obj):
        return obj.user.full_name

    user_name.short_description = "Name"

    def quiz_attempt_score(self,obj):
        if not obj.quiz_attempt:
            return None
        else:
            return obj.quiz_attempt.score
    quiz_attempt_score.admin_order_field = 'quiz_attempt__score'
