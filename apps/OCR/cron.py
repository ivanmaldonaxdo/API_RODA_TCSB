from django.shortcuts import render
from django.http import HttpResponse, response

def dicehola(request):
    print("esto es cron ")
    return HttpResponse("nuevamente provando cron")