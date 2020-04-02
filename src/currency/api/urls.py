from django.urls import path

from currency.api import views

app_name = 'api-currency'

urlpatterns = [
    path('rates/', views.RatesView.as_view(), name='rates'),
    path('rates/<int:pk>/', views.RateView.as_view(), name='rate'),

    path('contacts/', views.Contacts.as_view(), name='contacts'),
    path('contacts/<int:pk>', views.Contact.as_view(), name='contact'),
]
