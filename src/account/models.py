from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models


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


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(null=True, max_length=50)
    text = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

