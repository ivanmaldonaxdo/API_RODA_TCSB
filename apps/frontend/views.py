from django.shortcuts import render
from django.http import JsonResponse , request
import requests
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def processDocs(request):
    return render(request, 'frontend/inicio.html')  

def login(request):
    return render(request, 'frontend/login.html')

#@login_required
def homeinfo(request):
    return render(request, 'frontend/homeinfo.html')

