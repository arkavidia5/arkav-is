# Generated by Django 2.1.4 on 2019-01-18 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0002_auto_20190118_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='session_one_discounted_price',
        ),
        migrations.RemoveField(
            model_name='registrant',
            name='is_using_student_discount',
        ),
    ]
