# Generated by Django 2.2.10 on 2020-03-30 11:38

import account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200327_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message='it should be: +************', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.CreateModel(
            name='ActivationCodeSMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code', models.PositiveSmallIntegerField(default=account.models.generate_code)),
                ('is_activated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activation_sms_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
