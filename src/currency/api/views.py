from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from currency.api.serializers import (RateSerializer, FilterRate,
                                      ContactSerializer)

from currency.models import Rate
from account.models import Contact


class LargeResultsSetPagination(PageNumberPagination):  # https://www.django-rest-framework.org/api-guide/pagination/
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = FilterRate
    pagination_class = StandardResultsSetPagination


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = StandardResultsSetPagination


class Contacts(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(email=user.email)


class Contact(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


