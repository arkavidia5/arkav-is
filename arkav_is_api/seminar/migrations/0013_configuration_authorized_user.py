# Generated by Django 2.1.5 on 2019-02-08 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seminar', '0012_registrant_canceled_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='authorized_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]