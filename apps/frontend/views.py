from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, 'frontend/inicio.html')

def login(request):
    return render(request, 'frontend/login.html')