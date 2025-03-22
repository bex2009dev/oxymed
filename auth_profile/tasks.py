from celery import shared_task
from django.core.cache import cache 
from random import randint
from django.conf import settings
from django.core.mail import send_mail

from auth_profile.models import User

@shared_task
def user_email_message(email):
    code = str(randint(1000, 9000))
    send_mail("OXYmed", f'Your code is {code}', settings.EMAIL_HOST_USER, [email])
    cache.set(str(email), code, timeout=60)