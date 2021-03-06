# Generated by Django 2.1.4 on 2018-12-08 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0004_auto_20181205_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_participating', models.BooleanField(default=True)),
                ('start_time', models.TimeField()),
                ('finish_time', models.TimeField()),
                ('score', models.IntegerField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='quizparticipant',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizparticipant',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'Quizes'},
        ),
        migrations.AddField(
            model_name='quiz',
            name='max_attempt_per_user',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='quiz',
            name='question_per_attempt',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='quiz',
            name='randomize',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='QuizParticipant',
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
