# Generated by Django 2.1.5 on 2019-02-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0010_auto_20190124_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='reminder_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
