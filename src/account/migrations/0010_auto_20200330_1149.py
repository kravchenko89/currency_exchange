# Generated by Django 2.2.10 on 2020-03-30 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200330_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activationcodesms',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sms_codes', to=settings.AUTH_USER_MODEL),
        ),
    ]