from django.db import models

# Create your models here.
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

class Registrant(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS_SELECTION, default=0)
    is_register_session_one = models.BooleanField()
    is_register_session_two = models.BooleanField()
    payment_receipt = models.CharField(null=True, max_length=128, blank=True)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    registrant = models.ForeignKey(to=Registrant, on_delete=models.PROTECT)
    booking_number = models.CharField(max_length=8)
