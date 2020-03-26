from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse


@shared_task()
def send_email_task(subject, message,
                    email_from, recipient_list):
    send_mail(subject, message,
              email_from, recipient_list, fail_silently=False)


@shared_task()
def send_activation_code_async(email_to, code):
    path = reverse('account:activate', args=(code, ))

    send_mail(
        'Your activation code',
        f'http://127.0.0.1:8000{path}',
        'fenderoksp@gmail.com',
        [email_to],
        fail_silently=False,
    )


@shared_task()
def send_activation_code_sms(phone_to, code):
    send_mail(phone_to, fail_silently=False)
