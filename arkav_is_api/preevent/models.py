from django.db import models, transaction

# Create your models here.
from arkav_is_api.arkavauth.models import User
from arkav_is_api.quiz.models import Quiz, QuizParticipant, QuizAttempt

STATUS = (
    (1, 'PENDING'),
    (2, 'QUIZ_ATTEMPTED'),
    (3, 'QUIZ_FINISHED'),
    (4, 'ACCEPTED'),
    (5, 'REJECTED'),
)

QUIZ_SLUG = 'coding-class'

class Configuration(models.Model):
    is_coding_class_registration_open = models.BooleanField(default=False)
    coding_class_quiz_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Configuration, self).save(*args, **kwargs)


class CodingClassParticipant(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.PROTECT)
    birthday = models.DateField()
    domicile = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    grade = models.CharField(max_length=20)
    status = models.IntegerField(choices=STATUS)
    quiz_attempt = models.ForeignKey(to=QuizAttempt, on_delete= models.PROTECT,blank=True, null=True)
    def add_user_to_quiz_participant(self):
        with transaction.atomic():
            quiz = Quiz.objects.filter(slug=QUIZ_SLUG).first()
            QuizParticipant.objects.update_or_create(
                user = self.user,
                quiz = quiz,
                is_participating= True
            )

    def create_user_quiz_attempt(self):
        with transaction.atomic():
            quiz = Quiz.objects.filter(slug=QUIZ_SLUG).first()
            self.status = 2
            self.quiz_attempt = QuizAttempt.objects.create(
                user= self.user,
                quiz = quiz
            )

            self.save()

    def finish_quiz(self):
        with transaction.atomic():
            self.status = 3
            QuizAttempt.objects.filter(id=self.quiz_attempt_id).first().finish()
            self.save()