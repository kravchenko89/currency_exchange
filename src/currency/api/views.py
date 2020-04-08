from rest_framework import generics
from django_filters import rest_framework as filters

from currency.api.serializers import (RateSerializer, FilterRate,
                                      ContactSerializer)

from currency.models import Rate
from account.models import Contact


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = FilterRate


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class Contacts(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(email=user.email)


# class Contact(generics.RetrieveUpdateAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer

class Contact(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer