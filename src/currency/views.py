import csv

from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django_filters.views import FilterView
from django.core.cache import cache

from currency.filters import RateFilter
from currency.models import Rate
from currency import model_choices as mch
from currency.utils import genetere_rate_cache_key


class LatestRates(FilterView):
    filterset_class = RateFilter
    queryset = Rate.objects.all()
    template_name = 'rate.html'
    paginate_by = 10
    ordering = ['-created']
    context_object_name = 'rates'

    def get_context_data(self, *args, **kwargs):
        from urllib.parse import urlencode
        context = super().get_context_data(*args, **kwargs)

        query_params = dict(self.request.GET.items())
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = urlencode(query_params)

        return context

    # def get_paginate_by(self, queryset):
    #     super().get_paginate_by()

    # @property
    # def paginate_by(self):
    #     paginate = self.request.GET.get('paginate-by')
    #     return paginate


# Create your views here
class RateCSV(View):
    HEADERS = [
        'id',
        'created',
        'currency',
        'buy',
        'sale',
        'source',
    ]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        writer = csv.writer(response)

        writer.writerow(self.HEADERS)

        for rate in Rate.objects.all().iterator():
            row = [
                getattr(rate, f'get_{attr}_display')()
                if hasattr(rate, f'get_{attr}_display') else getattr(rate, attr)
                for attr in self.HEADERS
            ]

            writer.writerow(row)
            # writer.writerow(map(str, [
            #     rate.id,
            #     rate.created,
            #     rate.get_currency_display(),
            #     rate.buy,
            #     rate.sale,
            #     # rate.get_source_display(),
            # ]))

        return response


class LatestRate(TemplateView):
    template_name = 'latest-rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rates'] = Rate.objects.filter(course=mch.SR_PRIVAT, currency=mch.CURR_USD).last()
        # rates = {
        #     'privatBank': [Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_USD).last(),
        #                    Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_USD).last()],
        #     'MonoBank': [Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_USD).last(),
        #                  Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_USD).last()],

        rates = []
        for bank in mch.SOURCE_CHOICES:
            source = bank[0]
            for curr in mch.CURRENCY_CHOICES:
                currency = curr[0]
                cache_key = genetere_rate_cache_key(source, currency)

                rate = cache.get(cache_key)
                if rate is None:
                    rate = Rate.objects.filter(source=source, currency=currency).order_by('created').last()
                    if rate:
                        rate_dict = {
                            'currency': rate.currency,
                            'source': rate.source,
                            'sale': rate.sale,
                            'buy': rate.buy,
                            'created': rate.created,
                        }
                        rates.append(rate_dict)
                        cache.set(cache_key, rate_dict, 60 * 15)  # 15 minutes
                        # cache.set(cache_key, rate_dict, 5)  # 5 seconds
                else:
                    rates.append(rate)

            context['rates'] = rates
            # Rate.objects.filter(source=mch.SR_PRIVAT, currency=mch.CURR_USD).order_by('-created')[0]
            return context

'''
source PrivatBank - latest USD, latest UER
source MonoBank - latest USD, latest UER
'''
