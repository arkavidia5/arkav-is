# Generated by Django 2.1.3 on 2018-12-05 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20181205_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionselection',
            name='key',
            field=models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')], max_length=1),
        ),
        migrations.AlterUniqueTogether(
            name='questionselection',
            unique_together={('question', 'key')},
        ),
    ]
