import datetime
import random
import string

from django.core.mail import EmailMultiAlternatives
from django.db import models

# Create your models here.
from django.template.loader import get_template

from arkav_is_api.arkavauth.models import User


class Configuration(models.Model):
    is_registration_open = models.BooleanField(default=False)
    session_one_normal_price = models.IntegerField()
    session_two_price = models.IntegerField()
    session_one_max_capacity = models.IntegerField()
    session_one_current_capacity = models.IntegerField()
    session_two_max_capacity = models.IntegerField()
    session_two_current_capacity = models.IntegerField()

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Configuration, self).save(*args, **kwargs)
    def reserve_session_one(self):
        if(self.session_one_current_capacity < 1):
            raise Exception("Tiket pada sesi 1 sudah habis")
        else:
            self.session_one_current_capacity  = self.session_one_current_capacity - 1
            self.save()
    def reserve_session_two(self):
        if(self.session_two_current_capacity < 1):
            raise Exception("Tiket pada sesi 2 sudah habis")
        else:
            self.session_two_current_capacity  = self.session_two_current_capacity - 1
            self.save()
    def unreserve_session_one(self):
        self.session_one_current_capacity = self.session_one_current_capacity + 1
    def unreserve_session_two(self):
        self.session_two_current_capacity = self.session_two_current_capacity + 1


STATUS_SELECTION = (
    (0, 'Menunggu Pembayaran'),
    (1, 'Menunggu Validasi'),
    (2, 'Sukses'),
    (3, 'Dibatalkan'),
)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Registrant(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS_SELECTION, default=0)
    is_register_session_one = models.BooleanField()
    is_register_session_two = models.BooleanField()
    payment_receipt = models.CharField(null=True, max_length=128, blank=True)
    is_valid = models.BooleanField(default=False)
    reminder_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    def issue_ticket(self):
        self.status = 2
        if(self.is_valid):
            try:
                ticket = Ticket.objects.create(
                    registrant= self,
                    booking_number=id_generator()
                )
                ticket.send_mail()
            except Exception as err:
                pass
        self.save()

    def send_reminder(self):
        context = {
            'registrant': self,
            'expired': (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%d %b %Y")
        }
        text_template = get_template('payment_reminder.txt')
        html_template = get_template('payment_reminder.html')
        mail_text_message = text_template.render(context)
        mail_html_message = html_template.render(context)
        # print(mail_html_message)
        mail = EmailMultiAlternatives(
            subject='Reminder Pembayaran ArkavTalk Arkavidia 5.0',
            body=mail_text_message,
            to=[self.user.email]
        )
        mail.attach_alternative(mail_html_message, "text/html")
        self.reminder_sent = datetime.datetime.now()
        mail.send()
        self.save()

class Ticket(models.Model):
    registrant = models.OneToOneField(to=Registrant, on_delete=models.PROTECT)
    booking_number = models.CharField(max_length=6, unique=True)
    mail_sent = models.DateTimeField(null=True, blank=True)

    def send_mail(self):
        context = {
            'registrant': self.registrant,
            'booking_number': self.booking_number,
        }
        text_template = get_template('ticket_issued.txt')
        html_template = get_template('ticket_issued.html')
        mail_text_message = text_template.render(context)
        mail_html_message = html_template.render(context)
        # print(mail_html_message)
        mail = EmailMultiAlternatives(
            subject='Tiket ArkavTalk Arkavidia 5.0',
            body=mail_text_message,
            to=[self.registrant.user.email]
        )
        mail.attach_alternative(mail_html_message, "text/html")
        self.mail_sent = datetime.datetime.now()
        mail.send()
        self.save()
