# Generated by Django 2.1.2 on 2018-11-04 05:32

import arkav_is_api.arkavauth.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from string import ascii_letters
from django.utils.crypto import get_random_string


# Default value function manually copied here to maintain reference to this function,
# since this function is changed in the next migration
def generate_random_str(length=30):
    return get_random_string(length, allowed_chars=ascii_letters)


class Migration(migrations.Migration):

    dependencies = [
        ('arkavauth', '0002_auto_20181031_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmationAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=generate_random_str, max_length=30)),
                ('confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_confirmation_attempt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=generate_random_str, max_length=30)),
                ('used', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_attempt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
