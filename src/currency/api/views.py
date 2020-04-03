from rest_framework import generics

from currency.api.serializers import RateSerializer
from currency.models import Rate


class RatesView(generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateView(generics.RetrieveUpdateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

