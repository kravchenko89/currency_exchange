import django_filters
from account.tasks import send_email_task
from rest_framework import serializers
from django.conf import settings

from currency.models import Rate
from account.models import Contact


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'created',
            'get_currency_display',
            'currency',
            'buy',
            'sale',
            'get_source_display',
            'source'
        )
        extra_kwargs = {
            'currency': {'write_only': True},
            'source': {'write_only': True}
        }


class FilterRate(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'currency': ['exact', ],
            'source': ['exact', ],
            'created': ['exact', 'lt', 'lte', 'gt', 'gte', 'date__gte', 'year__gte', 'range', 'date__range']
        }


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'email',
            'title',
            'text',
            'created',
        )

    def create(self, validated_data):
        send_email_task.delay(
            validated_data['title'],
            validated_data['text'],
            settings.EMAIL_HOST_USER,
            [validated_data['email'], ]
        )
        return super().create(validated_data)

# Добавить фильтрацию на на вью /rates/ GET. Поля для фильтрации: created - exact, lt, lte, gt, gte + BONUS range,
# source - exact, currency - exact Реалтзовать функционал для ContactUs модели по аналогии rates. Отсылать письмо при
# сохранении обькта в базу. Показывать только записи связанные с request юзером. BONUS, добавть юнит тесты для АПИ.
