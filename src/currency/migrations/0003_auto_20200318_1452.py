# Generated by Django 2.2.10 on 2020-03-18 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_auto_20200303_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]