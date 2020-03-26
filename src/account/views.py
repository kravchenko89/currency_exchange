from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import CreateView, UpdateView, ListView, View

from account.forms import UserCreationForm
from account.models import User, Contact, ActivationCode
from account.tasks import send_email_task


class UserCreate(CreateView):
    form_class = UserCreationForm
    queryset = User.objects.all()
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


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(
            ActivationCode.objects.select_related('user'),
            code=activation_code, is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')


from django.conf import settings
from django.http import HttpResponse
from twilio.rest import Client


def broadcast_sms(request):
    message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                "yet? Grab it here: https://www.twilio.com/quest")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)