# Generated by Django 2.1.4 on 2018-12-08 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_attemptanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='finish_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='quizattempt',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
