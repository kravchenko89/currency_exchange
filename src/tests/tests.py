from decimal import Decimal

import pytest
from rest_framework.reverse import reverse
from django.core import mail

from account.models import Contact
from account.tasks import send_activation_code_sms
from currency.models import Rate
from currency.tasks import privat, mono, vkurse


# def test_sanity():
#     assert 200 == 200
#     # assert 200 == 201


@pytest.mark.django_db
def test_get_rates_list(api_client, user_create):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.login(user_create.username, user_create.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


# @pytest.mark.skip
@pytest.mark.django_db
def test_download_rates(client):
    response = client.get(reverse('currency:download-rates'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_send_email():
    send_activation_code_sms(1, '12345')
    emails = mail.outbox
    assert len(emails) == 1

    email = mail.outbox[0]
    assert email.subject == 'Your activation code'


@pytest.mark.django_db
def test_get_contact(api_client, user_create):
    url = reverse('api-currency:contacts')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_contact(api_client, user_create):
    url = reverse('api-currency:contacts')
    response = api_client.post(
        url,
        data={
            'email': 'vadimvadim@mail.com',
            'title': 'title',
            'text': 'text'
        },
        format='json'
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_dell_contact(api_client, user_create):
    url = reverse('api-currency:contacts')
    response = api_client.post(
        url,
        data={
            'email': 'vadimvadim@mail.com',
            'title': 'title',
            'text': 'text'
        },
        format='json'
    )
    Contact.objects.last().delete()

    assert response.status_code == 201


@pytest.mark.django_db
def test_put_contact(api_client, user_create):
    contact = Contact.objects.create(id=1, email='vadimvadim@mail.com',
                                     title='title', text='text')
    url = reverse('api-currency:contact', kwargs={'pk': contact.id})
    response = api_client.put(
        url,
        data={
            'email': 'new_vadimvadim@mail.com',
            'title': 'new_title',
            'text': 'new_text'
        },
        format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_put_contact(api_client, user_create):
    contact = Contact.objects.create(id=1, email='vadimvadim@mail.com',
                                     title='title', text='text')
    url = reverse('api-currency:contact', kwargs={'pk': contact.id})
    response = api_client.patch(
        url,
        data={
            'title': 'new_title',
            'text': 'new_text'
        },
        format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_put_contact(api_client, user_create):
    contact = Contact.objects.create(id=1, email='vadimvadim@mail.com',
                                     title='title', text='text')
    url = reverse('api-currency:contact', kwargs={'pk': contact.id})
    response = api_client.delete(url, data={}, format='json')

    assert response.status_code == 204


class Response:
    pass


@pytest.mark.django_db
def test_privat(mocker):
    def mock():
        response = Response()
        response.json = lambda: [
            {"ccy": "USD", "buy": 27.20, "sale": 27.50},
            {"ccy": "EUR", "buy": 29.00, "sale": 30.10},
            {"ccy": "RUR", "buy": 1.0, "sale": 1.2}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    privat()


@pytest.mark.django_db
def test_mono(mocker):
    def mock():
        response = Response()
        response.json = lambda: [
            {"currencyCodeA": 840, "currencyCodeB": 980, "rateBuy": 27.20, "rateSell": 27.50},
            {"currencyCodeA": 978, "currencyCodeB": 980, "rateBuy": 29.00, "rateSell": 30.10},
            {"currencyCodeA": 643, "currencyCodeB": 980, "rateBuy": 1.0, "rateSell": 1.2}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    mono()


@pytest.mark.django_db
def test_vkurse(mocker):
    def mock():
        response = Response()
        response.json = lambda: {
            'Dollar': {'buy': 26.95, 'sale': 27.10},
            'Euro': {'buy': 29.00, 'sale': 29.40},
            'Rub': {'buy': 0.340, 'sale': 0.350}
        }

        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    vkurse()
