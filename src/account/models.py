from datetime import datetime
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

from account.tasks import send_activation_code_async


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
    phone = models.CharField(max_length=20, null=True, blank=True)


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
        return diff.days > 7

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)
