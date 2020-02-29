import requests

from celery import shared_task
from decimal import Decimal
from bs4 import BeautifulSoup

from currency.models import Rate
from currency import model_choices as mch


def privat():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    r_json = response.json()

    for rate in r_json:
        if rate['ccy'] in {'USD', 'EUR'}:
            currency = mch.CURR_USD if rate['ccy'] == 'USD' else mch.CURR_EUR
            # currency = {
            #     'USD': 'mch.CURR_USD',
            #     'EUR': 'mch.CURR_EUR',
            # }[rate['ccy']]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']).__round__(2),
                'sale': Decimal(rate['sale']).__round__(2),
                'source': mch.SR_PRIVAT,
            }
            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()


def mono():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    r_json = response.json()

    for rate in r_json:
        if rate['currencyCodeA'] in {840, 978} and rate['currencyCodeB'] not in {840}:
            currency = mch.CURR_USD if rate['currencyCodeA'] == 840 else mch.CURR_EUR
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['rateBuy']).__round__(2),
                'sale': Decimal(rate['rateSell']).__round__(2),
                'source': mch.SR_MONO,
            }

            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_MONO).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()


def vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    r_json = response.json()

    for key, value in r_json.items():

        if key in {'Dollar', 'Euro'} and value:
            currency = mch.CURR_USD if key == 'Dollar' else mch.CURR_EUR

            # currency = {
            #     'Dollar': mch.CURR_USD,
            #     'Euro': mch.CURR_EUR,
            # }[key]

            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(value['buy']).__round__(2),
                'sale': Decimal(value['sale']).__round__(2),
                'source': mch.SR_VKURSE
            }
            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SR_VKURSE).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()


def pumb():
    page = requests.get("https://about.pumb.ua/ru/info/currency_converter")
    soup = BeautifulSoup(page.content, 'html.parser')
    usd = list(soup.select('.exchange-rate:first-of-type table tr:nth-of-type(2) td:not(:first-of-type)'))
    eur = list(soup.select('.exchange-rate:first-of-type table tr:nth-of-type(3) td:not(:first-of-type)'))

    rate_kwargs = {
        'currency': mch.CURR_USD,
        'buy': Decimal(usd[0].get_text().replace(',', '.')).__round__(2),
        'sale': Decimal(usd[1].get_text().replace(',', '.')).__round__(2),
        'source': mch.SR_PUMB
    }

    new_rate = Rate(**rate_kwargs)
    last_rate = Rate.objects.filter(currency=mch.CURR_USD, source=mch.SR_PUMB).last()

    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()

    rate_kwarg = {
        'currency': mch.CURR_EUR,
        'buy': Decimal(eur[0].get_text().replace(',', '.')).__round__(2),
        'sale': Decimal(eur[1].get_text().replace(',', '.')).__round__(2),
        'source': mch.SR_PUMB
    }

    new_rate = Rate(**rate_kwarg)
    last_rate = Rate.objects.filter(currency=mch.CURR_EUR, source=mch.SR_PUMB).last()

    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


def btabank():
    page = requests.get("http://btabank.ua/ukr/main.php")
    soup = BeautifulSoup(page.content, 'html.parser')
    usd = list(soup.select(".curr table tr:nth-of-type(3) td:nth-of-type(2) span,"
                           " .curr table tr:nth-of-type(3) td:nth-of-type(3) span "))
    eur = list(soup.select(".curr table tr:nth-of-type(2) td:nth-of-type(2) span,"
                           " .curr table tr:nth-of-type(2) td:nth-of-type(3) span "))

    rate_kwargs = {
        'currency': mch.CURR_USD,
        'buy': Decimal(usd[0].get_text().replace(',', '.')).__round__(2),
        'sale': Decimal(usd[1].get_text().replace(',', '.')).__round__(2),
        'source': mch.SR_BTABANK
    }

    new_rt = Rate(**rate_kwargs)
    last_rt = Rate.objects.filter(currency=mch.CURR_USD, source=mch.SR_BTABANK).last()

    if last_rt is None or (new_rt.buy != last_rt.buy or new_rt.sale != last_rt.sale):
        new_rt.save()

    rate_kwarg = {
        'currency': mch.CURR_EUR,
        'buy': Decimal(eur[0].get_text().replace(',', '.')).__round__(2),
        'sale': Decimal(eur[1].get_text().replace(',', '.')).__round__(2),
        'source': mch.SR_BTABANK
    }

    new_rate = Rate(**rate_kwarg)
    last_rate = Rate.objects.filter(currency=mch.CURR_EUR, source=mch.SR_BTABANK).last()

    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


def oschad():
    page = requests.get("https://www.oschadbank.ua/ua")
    soup = BeautifulSoup(page.content, 'html.parser')

    rate_kwargs = {
        'currency': mch.CURR_USD,
        'buy': Decimal(soup.find('strong', class_='buy-USD').text.strip()).__round__(2),
        'sale': Decimal(soup.find('strong', class_='sell-USD').text.strip()).__round__(2),
        'source': mch.SR_OSCHADBANK
    }

    new_rt = Rate(**rate_kwargs)
    last_rt = Rate.objects.filter(currency=mch.CURR_USD, source=mch.SR_OSCHADBANK).last()

    if last_rt is None or (new_rt.buy != last_rt.buy or new_rt.sale != last_rt.sale):
        new_rt.save()

    rate_kwarg = {
        'currency': mch.CURR_EUR,
        'buy': Decimal(soup.find('strong', class_='buy-EUR').text.strip()).__round__(2),
        'sale': Decimal(soup.find('strong', class_='sell-EUR').text.strip()).__round__(2),
        'source': mch.SR_OSCHADBANK
    }

    new_rate = Rate(**rate_kwarg)
    last_rate = Rate.objects.filter(currency=mch.CURR_EUR, source=mch.SR_OSCHADBANK).last()

    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


@shared_task()
def parse_rates():
    privat()
    mono()
    vkurse()
    pumb()
    btabank()
    oschad()

# soup.select('.exchange-rate:first-of-type table tr:nth-of-type(2) td:not(:first-of-type)')
# Out[32]: [<td>24.45</td>, <td>24.70</td>]
#
#
#
#
#  soup.select('.exchange-rate:first-of-type table tr:nth-of-type(3) td:not(:first-of-type)')
# Out[33]: [<td>26.75</td>, <td>27.05</td>]
#
