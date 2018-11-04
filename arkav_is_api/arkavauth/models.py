from string import ascii_letters
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


def generate_random_str(length=30):
    return get_random_string(length, allowed_chars=ascii_letters)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=75)
    email = models.EmailField(_('email address'), unique=True)
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class EmailConfirmationAttempt(models.Model):
    """
    An attempt to confirm email
    """
    user = models.OneToOneField(to=User, related_name='email_confirmation_attempt', on_delete=models.CASCADE)
    token = models.CharField(max_length=30, default=generate_random_str)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def send_email(self):
        link = 'https://arkavidia.id/confirm-email/%s' % (self.token)

        mail_subject = 'Email Confirmation'
        mail_message = 'One last step to use your account!'
        mail_from = 'Arkavidia 5 <noreply@arkavidia.id>'
        mail_to = self.user.email
        # TODO: make good html message
        mail_html_message = 'Click <a href="%s"> here </a> to confirm your password' % (link)

        send_mail(mail_subject, mail_message, mail_from, [mail_to], html_message=mail_html_message, fail_silently=False)

    def confirm(self):
        self.confirmed = True
        self.save()

        user = self.user
        user.email_confirmed = True
        user.save()


class PasswordResetAttempt(models.Model):
    """
    An attempt to reset password.
    """
    user = models.OneToOneField(to=User, related_name='password_reset_attempt', on_delete=models.CASCADE)
    token = models.CharField(max_length=30, default=generate_random_str)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def generate_new_token(self):
        self.token = generate_random_str()
        self.used = False
        self.save()

    def send_email(self):
        link = 'https://arkavidia.id/reset-password/%s' % (self.token)

        mail_subject = 'Password Reset'
        mail_message = 'Reset your password'
        mail_from = 'Arkavidia 5 <noreply@arkavidia.id>'
        mail_to = self.user.email
        # TODO: make good html message
        mail_html_message = 'Click <a href="%s"> here </a> to reset your password' % (link)

        send_mail(mail_subject, mail_message, mail_from, [mail_to], html_message=mail_html_message, fail_silently=False)
