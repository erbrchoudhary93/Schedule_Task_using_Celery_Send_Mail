
from django.urls import path
from . import views

urlpatterns = [
    path('mail/', views.send_mail_to_all),
    path('schedulemail/', views.send_mail_at_particular_time),
    # path('mailbeat/', views.send_mail_to_all_with_beats),
    
]
    
