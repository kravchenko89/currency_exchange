from django.urls import path

from currency import views

app_name = 'currency'

urlpatterns = [
    path('rate/', views.LatestRates.as_view(), name='latest-rates'),
    path('download/rates/', views.RateCSV.as_view(), name='download-rates'),
    path('latest/rate/', views.LatestRate.as_view(), name='latest-rat'),
]
