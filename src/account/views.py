from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import CreateView, UpdateView, ListView, View

from account.forms import UserCreationForm
from account.models import User, Contact
from account.tasks import send_email_task
from currency.models import Rate


# from django.views.generic import TemplateView

# class AboutView(TemplateView):
#     template_name = '...'
#
#     def get(self, request):
#         pass
#
#     def post(self):
#         pass

class UserCreate(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/singup.html'


class UserLogin(LoginView):
    model = User
    fields = ['username', 'password']
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')


class EmailUs(CreateView):
    model = Contact
    template_name = 'my_profile.html'
    queryset = Contact.objects.all()
    fields = ('email', 'title', 'text')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_email_task.delay(subject=self.object.title, message=self.object.text,
                              email_from=self.object.email, recipient_list=[settings.EMAIL_HOST_USER, ])
        return response


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', 'username')
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)
