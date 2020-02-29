from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from account.forms import UserCreationForm


def smoke(request):
    # use only with 8001 port
    # breakpoint()
    return HttpResponse('smoke')


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
