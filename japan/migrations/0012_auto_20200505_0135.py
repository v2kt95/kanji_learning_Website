# Generated by Django 2.2.9 on 2020-05-05 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('japan', '0011_timereset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanji',
            name='other_information',
            field=models.CharField(default='', max_length=500),
        ),
    ]
