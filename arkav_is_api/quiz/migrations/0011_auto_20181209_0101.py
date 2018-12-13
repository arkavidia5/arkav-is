# Generated by Django 2.1.4 on 2018-12-08 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0010_auto_20181209_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_participating', models.BooleanField(default=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='quizattempt',
            name='is_participating',
        ),
    ]