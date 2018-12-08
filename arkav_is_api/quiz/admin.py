from django.contrib import admin
from .models import Quiz, Question, QuestionSelection, QuizAttempt, AttemptAnswer
import nested_admin


def finish(model, request, queryset):
    for item in queryset:
        item.finish()


finish.short_description = "Finish all attempt"


def regrade(model, request, queryset):
    for item in queryset:
        item.grade()


regrade.short_description = "Regrade all finished attempt"


class QuestionSelectionInline(nested_admin.NestedTabularInline):
    model = QuestionSelection
    max_num = 5


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [
        QuestionSelectionInline
    ]

@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        QuestionInline,
    ]
    list_display = ('name', 'is_open', 'is_publicg')


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    readonly_fields = [
        'question_description'
    ]
    def question_description(self, obj):
        return obj.question.description



@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    inlines = [
        AttemptAnswerInline
    ]
    actions = [
        finish, regrade
    ]
    list_display = ('quiz', 'user', 'start_time', 'finish_time', 'score')
    pass

