from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [

    path('registration/', views.UserCreate.as_view(), name='registration'),
    path('email-new/', views.EmailUs.as_view(), name='email-new'),
    path('profile/<int:pk>/', views.MyProfile.as_view(), name='my-profile'),
]
