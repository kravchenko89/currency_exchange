from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [

    path('registration/', views.UserCreate.as_view(), name='registration'),
    path('email-new/', views.EmailUs.as_view(), name='email-new'),
    path('profile/<int:pk>/', views.MyProfile.as_view(), name='my-profile'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('activate/<uuid:activation_code>/', views.Activate.as_view(), name='activate'),

    url(r'broadcast$', views.broadcast_sms, name="default"),
]
