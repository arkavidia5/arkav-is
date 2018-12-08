from django.contrib import admin

# Register your models here.
from arkav_is_api.preevent.models import CodingClassParticipant
from arkav_is_api.quiz.models import QuizAttempt


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
    readonly_fields = ('user_name',)

    def user_name(self,obj):
        return obj.user.full_name

    user_name.short_description = "Name"

    def quiz_attempt_score(self,obj):
        return obj.quiz_attempt.score