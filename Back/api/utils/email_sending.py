from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect

from Config.settings import EMAIL_HOST_USER


def custom_send_email(subject: str, message: str, destination: list, addressee: str = ''):
        send_mail(subject,
                  message,
                  addressee,
                  destination,
                  fail_silently=False)
