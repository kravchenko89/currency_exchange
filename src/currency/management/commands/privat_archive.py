from django.core.management.base import BaseCommand

import requests

from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY

from decimal import Decimal

from currency import model_choices as mch
from currency.models import Rate


class Command(BaseCommand):
    help = 'privat_archive'

    def handle(self, *args, **options):
        b = date.today()
        a = date.today() - relativedelta(years=4)

        for dt in rrule(DAILY, dtstart=a, until=b):
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date=' \
                  f'{dt.strftime("%d-%m-%Y").replace("-", ".")}'
            response = requests.get(url)
            r_json = response.json()
            for rate in r_json['exchangeRate']:
                if 'currency' in rate:
                    if rate['currency'] in {'USD', 'EUR'}:
                        if 'purchaseRate' in rate and 'saleRate' in rate:

                            currency = mch.CURR_USD if rate['currency'] == 'USD' else mch.CURR_EUR
                            rate_kwargs = {
                                'created': dt,
                                'currency': currency,
                                'buy': Decimal(rate['purchaseRate']).__round__(2),
                                'sale': Decimal(rate['saleRate']).__round__(2),
                                'source': mch.SR_PRIVAT,
                            }
                            new_rate = Rate(**rate_kwargs)
                            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).last()

                            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                                new_rate.save()
