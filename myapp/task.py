
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from send_mail_with_celery import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self,*args):
    users = get_user_model().objects.all()
    # timezone.localtime(users.date_time)
    for user in users:
        mail_subject = "Hii This is Celery Testing"
        message = "Celery Test successfully now i can send mail using celery and also i can schudle task"
        to_email= user.email
        send_mail(
            subject=mail_subject,
            message = message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True
        )
    return "Mail sent successfully"

@shared_task(bind=True)
def send_mail_func_with_beats(self):
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "Hii This is Celery Beat Testing"
        message = "Celery Test successfully now i can send mail using celery Beats and i  schudle task  On 9:05AM"
        to_email= user.email
        send_mail(
            subject=mail_subject,
            message = message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True
        )
    return "Mail sent successfully"
