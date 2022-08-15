# **Schedule Task Using Celery**

## configuration in settings.py file

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'django_celery_results',
    'django_celery_beat',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'send_email_celery',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


TIME_ZONE = 'Asia/Kolkata'

# CELERY SETTINGS

CELERY_BROKER_URL ='redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT= ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE='Asia/Kolkata'


#celery results setting
CELERY_RESULT_BACKEND = 'django-db'


# celery beat settings

CELERY_BEAT_SCHEDULER ='django_celery_beat.schedulers:DatabaseScheduler'


# smtp setting

EMAIL_USE_TLS =True
EMAIL_HOST ='smtp.gmail.com'
EMAIL_HOST_USER = 'erbrchoudhary0789@gmail.com'
EMAIL_HOST_PASSWORD = "qfuozyucrnpsndgs"
EMAIL_PORT = 587
EMAIL_BACKEND= "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL= 'erbrchoudhary0789@gmail.com'
EMAIL_USER_SSL = False


```

## configuration in __init__.py file

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```
## configuration in celery.py file
```python
from __future__ import absolute_import ,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','send_mail_with_celery.settings')
app=Celery('send_mail_with_celery')


#celery beat settings
app.conf.enable_utc =False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')
app.autodiscover_tasks()

# CELERY Beat Settings
app.conf.beat_schedule ={
    'send-mail-everyday-at-8':{
        'task':'myapp.task.send_mail_func_with_beats',
        'schedule':crontab(hour=9,minute=5,day_of_month=13,month_of_year=8),
        
        }
    
    }
@app.task(bind=True)
def debug_task(self):
    print(f'Request : {self.request!r}')
    
 
```
## configuration in urls.py file

```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('myapp.urls'))
]

```

## configuration in myapp/task.py file

```python

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from send_mail_with_celery import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self,*args):
    users = get_user_model().objects.all()
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

```
## configuration in myapp/urls.py file

```python
from django.urls import path
from . import views

urlpatterns = [
    path('mail/', views.send_mail_to_all),
    path('schedulemail/', views.send_mail_at_particular_time),
  ),
    
]
    
```

## configuration in myapp/views.py file

```python
from django.shortcuts import render
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import json
from django.http import HttpResponse
from .task  import send_mail_func,send_mail_func_with_beats

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("mail sent")
    
def send_mail_at_particular_time(request):
    schedule,created =CrontabSchedule.objects.get_or_create(hour=15,minute=52)
    task = PeriodicTask.objects.create(crontab=schedule,name="schedule_mail_task"+"d", task='myapp.task.send_mail_func' ,args=json.dumps([[2,3]],))
    return HttpResponse("mail secduled")

```



