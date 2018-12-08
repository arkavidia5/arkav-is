# Generated by Django 2.1.4 on 2018-12-08 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_auto_20181209_0217'),
        ('preevent', '0002_codingclassparticipant_quiz_attempt_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codingclassparticipant',
            name='quiz_attempt_id',
        ),
        migrations.AddField(
            model_name='codingclassparticipant',
            name='quiz_attempt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='quiz.QuizAttempt'),
        ),
    ]
