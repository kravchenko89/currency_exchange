import csv

from django.http import HttpResponse
from django.views.generic import View
from django.urls import reverse_lazy
from django_filters.views import FilterView

from currency.filters import RateFilter
from currency.models import Rate


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
