from django.contrib import admin
from .models import Quiz, Question, QuestionSelection
import nested_admin

# Register your models here.


class QuestionSelectionInline(nested_admin.NestedTabularInline):
    model = QuestionSelection
    max_num = 5
class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [
        QuestionSelectionInline
    ]

@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        QuestionInline,
    ]

