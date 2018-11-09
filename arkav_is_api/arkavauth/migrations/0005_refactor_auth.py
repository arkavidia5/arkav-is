import arkav_is_api.arkavauth.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arkavauth', '0004_user_email_confirmed'),
    ]

    operations = [
        migrations.RenameModel('EmailConfirmationAttempt', 'RegistrationConfirmationAttempt'),
        migrations.RenameModel('PasswordResetAttempt', 'PasswordResetConfirmationAttempt'),
        migrations.RenameField(
            model_name='user',
            old_name='email_confirmed',
            new_name='is_email_confirmed',
        ),
        migrations.RenameField(
            model_name='passwordresetconfirmationattempt',
            old_name='used',
            new_name='is_confirmed',
        ),
        migrations.RenameField(
            model_name='registrationconfirmationattempt',
            old_name='confirmed',
            new_name='is_confirmed',
        ),
        migrations.AddField(
            model_name='passwordresetconfirmationattempt',
            name='email_last_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrationconfirmationattempt',
            name='email_last_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='passwordresetconfirmationattempt',
            name='token',
            field=models.CharField(default=arkav_is_api.arkavauth.models.generate_email_confirmation_token, max_length=30),
        ),
        migrations.AlterField(
            model_name='passwordresetconfirmationattempt',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_confirmation_attempt', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='registrationconfirmationattempt',
            name='token',
            field=models.CharField(default=arkav_is_api.arkavauth.models.generate_email_confirmation_token, max_length=30),
        ),
        migrations.AlterField(
            model_name='registrationconfirmationattempt',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registration_confirmation_attempt', to=settings.AUTH_USER_MODEL),
        ),
    ]
