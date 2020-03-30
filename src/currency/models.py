from datetime import datetime
from django.db import models

from currency import model_choices as mch


class Rate(models.Model):
    created = models.DateTimeField(default=datetime.now, editable=False)
    currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
    buy = models.DecimalField(max_digits=4, decimal_places=2)
    sale = models.DecimalField(max_digits=4, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)

    def __str__(self):
        return f'{self.get_source_display()} {self.created} {self.get_currency_display()} {self.buy} {self.sale}'
