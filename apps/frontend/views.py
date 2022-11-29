from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.management.models import Sucursal, Proveedor, Servicio
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

def cron(request):
    return render(request,'frontend/cron.html')
    
def Cliente(request):
    return render(request, 'frontend/Cliente.html')

def modificarcliente(request):
    return render(request, 'frontend/modificarcliente.html')

def listarcliente(request):
    return render(request, 'frontend/listarcliente.html')

def Usuarios(request):
    return render(request, 'frontend/Usuarios.html')

def modificarusuario(request):
    return render(request, 'frontend/modificarusuario.html')

def listarusuarios(request):
    return render(request, 'frontend/listarusuarios.html')

def servicio_cliente(request):
    sucursales = Sucursal.objects.all()
    proveedor = Proveedor.objects.all()
    context = {'sucu': sucursales, 'prov':proveedor}
    return render(request, 'frontend/contrato_servicio.html', context)

def cron(request):
    return render(request, 'frontend/cron.html')

def log(request):
    return render(request, 'frontend/log.html')

def proveedores(request):
    servicio = Servicio.objects.all()
    context = {'serv': servicio}
    return render(request, 'frontend/proveedores.html', context)

def Sucursales(request):
    return render(request, 'frontend/sucursales.html')

def listarSucursales(request):
    return render(request, 'frontend/listarSucursales.html')
