from django.shortcuts import render
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import json

# Create your views here.from django.shortcuts import render
from django.http import HttpResponse
from .task  import send_mail_func,send_mail_func_with_beats

# Create your views here.
# def test(request):
#     test_func.delay()
#     return HttpResponse ("Done")

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("mail sent")


# def send_mail_to_all_with_beats(request):
#     send_mail_func_with_beats.delay()
#     return HttpResponse("mail sent")
    
    
def send_mail_at_particular_time(request):
    schedule,created =CrontabSchedule.objects.get_or_create(hour=15,minute=28)
    task = PeriodicTask.objects.create(crontab=schedule,name="schedule_mail_task"+"c", task='myapp.task.send_mail_func' ,args=json.dumps([[2,3]],))
    return HttpResponse("mail secduled")
