from string import ascii_letters, digits
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# TODO: email confirmation expiry


def generate_email_confirmation_token(length=30):
    return get_random_string(length, allowed_chars=ascii_letters + digits)


class UserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    User model.
    """
    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=75)
    email = models.EmailField(_('email address'), unique=True)
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class RegistrationConfirmationAttempt(models.Model):
    """
    An attempt to confirm registration using email.
    """
    user = models.OneToOneField(to=User, related_name='registration_confirmation_attempt', on_delete=models.CASCADE)
    token = models.CharField(max_length=30, default=generate_email_confirmation_token)
    is_confirmed = models.BooleanField(default=False)
    email_last_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.user.full_name, self.user.email)

    def send_email(self):
        context = {
            'user': self.user,
            'token': self.token,
        }
        text_template = get_template('registration_confirmation_email.txt')
        html_template = get_template('registration_confirmation_email.html')
        mail_text_message = text_template.render(context)
        mail_html_message = html_template.render(context)

        mail = EmailMultiAlternatives(
            subject='Konfirmasi Email',
            body=mail_text_message,
            to=[self.user.email]
        )
        mail.attach_alternative(mail_html_message, "text/html")
        mail.send()
        self.email_last_sent_at = timezone.now()
        self.save()


class PasswordResetConfirmationAttempt(models.Model):
    """
    An attempt to confirm password reset using email.
    """
    user = models.OneToOneField(to=User, related_name='password_reset_confirmation_attempt', on_delete=models.CASCADE)
    token = models.CharField(max_length=30, default=generate_email_confirmation_token)
    is_confirmed = models.BooleanField(default=False)
    email_last_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.user.full_name, self.user.email)

    def send_email(self):
        context = {
            'user': self.user,
            'token': self.token,
        }
        text_template = get_template('password_reset_confirmation_email.txt')
        html_template = get_template('password_reset_confirmation_email.html')
        mail_text_message = text_template.render(context)
        mail_html_message = html_template.render(context)

        mail = EmailMultiAlternatives(
            subject='Reset Password',
            body=mail_text_message,
            to=[self.user.email]
        )
        mail.attach_alternative(mail_html_message, "text/html")
        mail.send()
        self.email_last_sent_at = timezone.now()
        self.save()
