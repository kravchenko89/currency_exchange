from datetime import datetime
from django.db import models
from django.core.cache import cache


from currency import model_choices as mch
from currency.utils import genetere_rate_cache_key


class Rate(models.Model):
    created = models.DateTimeField(default=datetime.now, editable=False)
    currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
    buy = models.DecimalField(max_digits=4, decimal_places=2)
    sale = models.DecimalField(max_digits=4, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)

    def __str__(self):
        return f'{self.get_source_display()} {self.created} {self.get_currency_display()} {self.buy} {self.sale}'

    def save(self, *args, **kwargs):
        if not self.id:
            cache_key = genetere_rate_cache_key(self.source, self.currency)
            cache.delete(cache_key)

        super().save(*args, **kwargs)
        # after
