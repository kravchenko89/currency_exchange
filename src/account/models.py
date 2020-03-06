from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(null=True, max_length=50)
    text = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
