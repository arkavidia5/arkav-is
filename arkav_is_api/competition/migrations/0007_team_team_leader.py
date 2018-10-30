# Generated by Django 2.1.2 on 2018-10-29 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competition', '0006_task_response_last_submitted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_leader',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.PROTECT, related_name='team_leader', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
