from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def processDocs(request):
    return render(request, 'frontend/processDocs.html')  

def login(request):
    return render(request, 'frontend/login.html')

@login_required
def homeinfo(request):
    return render(request, 'frontend/homeinfo.html')

@login_required
def processed(request):
    return render(request, 'frontend/processed.html')

def Cliente(request):
    return render(request, 'frontend/Cliente.html')

def Usuarios(request):
    return render(request, 'frontend/Usuarios.html')


def test(request):
    return render(request, 'frontend/test.html')

