# Generated by Django 2.1.7 on 2019-07-14 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammar', '0002_sentence__content'),
    ]

    operations = [
        migrations.AddField(
            model_name='grammar',
            name='_level',
            field=models.IntegerField(default=1),
        ),
    ]
