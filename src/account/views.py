from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.views.generic import CreateView, UpdateView, ListView

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

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserCreate(generic.CreateView):
    model = User
    fields = ['username', 'email']
    template_name = 'registration/registration.html'
    pass


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
    fields = ('email', )
    slug_url_kwarg = reverse_lazy('index')


class LatestRates(ListView):
    model = Rate
    template_name = 'rate.html'
    queryset = Rate.objects.all().order_by('-id')[:20][::-1]
    context_object_name = 'rates'
    slug_url_kwarg = reverse_lazy('index')
