# Generated by Django 2.1.4 on 2019-01-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0004_auto_20190118_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrant',
            name='status',
            field=models.IntegerField(choices=[(0, 'Menunggu Pembayaran'), (1, 'Sukses'), (-1, 'Dibatalkan')], default=1),
        ),
    ]
