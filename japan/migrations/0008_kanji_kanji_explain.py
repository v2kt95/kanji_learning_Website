# Generated by Django 2.2.6 on 2019-11-23 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('japan', '0007_auto_20190514_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanji',
            name='kanji_explain',
            field=models.CharField(default='', max_length=500),
        ),
    ]