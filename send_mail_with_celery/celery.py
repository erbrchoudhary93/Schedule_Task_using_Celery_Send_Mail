from __future__ import absolute_import ,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# from django_celery_beat.models  import PeriodicTask




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
    
 