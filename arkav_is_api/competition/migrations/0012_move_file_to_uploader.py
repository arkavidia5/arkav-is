# Generated by Django 2.1.2 on 2018-11-04 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0011_competition_categories'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
        migrations.AlterModelOptions(
            name='competitioncategory',
            options={'verbose_name': 'competition category', 'verbose_name_plural': 'competition categories'},
        ),
    ]
