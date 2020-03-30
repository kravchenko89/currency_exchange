from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import CreateView, UpdateView, FormView

from account.forms import UserCreationForm, ActivateForm
from account.models import User, Contact, ActivationCodeSMS
from account.tasks import send_email_task


class UserCreate(CreateView):
    form_class = UserCreationForm
    queryset = User.objects.all()
    success_url = reverse_lazy('account:activate')
    template_name = 'registration/singup.html'

    def get_success_url(self):
        self.request.session['user_id'] = self.object.id
        return super().get_success_url()


class Activate(FormView):
    form_class = ActivateForm
    template_name = 'sms_code.html'

    def post(self, request):
        user_id = request.session['user_id']
        sms_code = request.POST['sms_code']
        ac = get_object_or_404(
            ActivationCodeSMS.objects.select_related('user'),
            code=sms_code,
            user_id=user_id,
            is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])

        return redirect('index')


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
