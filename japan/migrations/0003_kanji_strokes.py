# Generated by Django 2.1.7 on 2019-03-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('japan', '0002_word_remember_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanji',
            name='strokes',
            field=models.IntegerField(default=0),
        ),
    ]
