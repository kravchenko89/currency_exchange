import os
import shutil

from django.db.models.signals import pre_save
from django.dispatch import receiver
from currency_exchange.settings import MEDIA_ROOT

from account.models import User


@receiver(pre_save, sender=User)
def del_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = User.objects.get(pk=instance.pk).avatar
        except User.DoesNotExist:
            return
        else:
            new_avatar = instance.avatar
            if old_avatar and old_avatar.url != new_avatar.url:
                old_avatar.delete(save=False)
