# Generated by Django 2.2.10 on 2020-03-27 10:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20200325_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message='it should be: +380*********', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
