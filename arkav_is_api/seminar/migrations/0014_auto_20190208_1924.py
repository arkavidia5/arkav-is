# Generated by Django 2.1.5 on 2019-02-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0013_configuration_authorized_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='check_in_session_one',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='check_in_session_two',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]