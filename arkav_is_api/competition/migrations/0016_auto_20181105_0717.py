# Generated by Django 2.1.3 on 2018-11-05 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0015_auto_20181105_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='filename',
            field=models.CharField(max_length=120),
        ),
    ]