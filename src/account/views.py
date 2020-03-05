from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from account.forms import UserCreationForm
from account.models import User

# class AboutView(TemplateView):
#     template_name = '...'
#
#     def get(self, request):
#         pass
#
#     def post(self):
#         pass


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserCreate(generic.CreateView):
    model = User
    fields = ['username', 'email']
    template_name = 'registration/registration.html'
    pass
