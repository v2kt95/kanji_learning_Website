# Generated by Django 2.1.7 on 2019-05-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('japan', '0004_auto_20190511_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanji',
            name='day_count',
            field=models.IntegerField(default=1),
        ),
    ]
