# Generated by Django 2.1.7 on 2019-05-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('japan', '0006_timereview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timereview',
            name='NextTimeReview',
            field=models.DateTimeField(blank=True),
        ),
    ]
