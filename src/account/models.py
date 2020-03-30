from datetime import datetime
from random import randint
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from account.tasks import send_activation_code_async, send_activation_code_sms  # send_activation_sms_code_async


def avatar_path(instance, filename: str) -> str:
    # ext = filename.split('.')[-1]  # or _,
    # f = str(uuid4())
    # filename = f'{f}.{ext}'
    # return '/'.join(['hello', filename])
    return '/'.join(['avatar', str(instance.id), str(uuid4()), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path,
                               null=True, blank=True,
                               default=None)
    valid_phone = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='it should be: +************')  # нашел в сети
    phone = models.CharField(validators=[valid_phone], max_length=17, null=True, blank=True)


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(null=True, max_length=50)
    text = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 5

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)


def generate_code():
    return randint(1000, 32000)


class ActivationCodeSMS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.PositiveSmallIntegerField(default=generate_code)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 5

    def send_activation_code_sms(self):
        import os
        from twilio.rest import Client
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=f'enter the code from SMS to activate your account{self.code}',
            from_=settings.MY_PHONE_NUMBER,
            to=self.user.phone
        )
        send_activation_code_sms.delay(self.user.phone, self.code)
