from django.db import models

# Create your models here.
from arkav_is_api.arkavauth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=128)
    is_public = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    max_attempt_per_user = models.IntegerField(default=1)
    randomize = models.BooleanField(default=False)
    question_per_attempt = models.IntegerField(default=5)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Quizes"


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    is_participating = models.BooleanField(default=True)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    score = models.IntegerField(null=True)


class Question(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.PROTECT)
    description = models.TextField()
    def __str__(self):
        return '%s - %s' % (self.quiz, self.id)


class QuestionSelection(models.Model):
    QUIZ_SELECTION = (
        ('a', 'A'),
        ('b','B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
    )
    question = models.ForeignKey(to=Question, on_delete=models.PROTECT)
    key = models.CharField(max_length=1, null=False, choices=QUIZ_SELECTION)
    value = models.CharField(max_length=128, null=False)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'key')
    def __str__(self):
        return '%s : %s - %s' % (self.question, self.get_key_display(),self.value)