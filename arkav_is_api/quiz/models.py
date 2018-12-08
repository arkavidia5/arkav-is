import datetime

from django.db import models, transaction

# Create your models here.
from django.db.models.signals import post_save

from arkav_is_api.arkavauth.models import User

QUIZ_SELECTION = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
)

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

class QuizParticipant(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    is_participating = models.BooleanField(default=True)

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    start_time = models.TimeField(null=True, blank=True)
    finish_time = models.TimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    def post_create(sender, instance, created, **kwargs):
        if not created:
            pass
        else:
            with transaction.atomic():
                instance.start_time = datetime.datetime.now()
                if instance.quiz.randomize:
                    for question in instance.quiz.question_set.all().order_by('?')[:instance.quiz.question_per_attempt]:
                        AttemptAnswer.objects.create(
                            attempt = instance,
                            question = question
                        )
                instance.save()

    def grade(self):
        if not self.finish_time:
            pass
        else:
            with transaction.atomic():
                count = 0
                correct = 0
                for attempt in self.attemptanswer_set.all():
                    count = count + 1
                    if not attempt.answer:
                        pass
                    else:
                        if attempt.question.questionselection_set.filter(key__exact=attempt.answer).first().is_correct:
                            correct = correct + 1
                self.score = 100 * (correct/count)
                self.save()

    def finish(self):
        with transaction.atomic():
            self.finish_time = datetime.datetime.now()
            self.grade()
            self.save()



class Question(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.PROTECT)
    description = models.TextField()
    def __str__(self):
        return '%s - %s' % (self.quiz, self.id)


class QuestionSelection(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.PROTECT)
    key = models.CharField(max_length=1, null=False, choices=QUIZ_SELECTION)
    value = models.CharField(max_length=128, null=False)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'key')
    def __str__(self):
        return '%s : %s - %s' % (self.question, self.get_key_display(),self.value)
class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(to=QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.PROTECT)
    answer = models.CharField(max_length=1, choices=QUIZ_SELECTION, blank=True, null=True)

    class Meta:
        unique_together = ('attempt', 'question')

post_save.connect(QuizAttempt.post_create, sender=QuizAttempt)
