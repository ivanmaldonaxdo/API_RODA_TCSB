
from django.urls import path
from .views import *

urlpatterns = [
    path('process/', processDocs, name="process"),
    path('', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo"),
    path('processedDocs/', processed, name="processed"),
    path('Cliente/', Cliente, name="Cliente"),
    path('Modificarcliente/', modificarcliente, name="modificarcliente"),
    path('listarcliente/', listarcliente, name="listarcliente"),
    path('registrar-usuarios/', Usuarios, name="Usuarios"),
    path('Modificarusuario/', modificarusuario, name="modificarusuario"),
    path('registrarcontrato/', servicio_cliente, name="registrarcontrato"),
    path('registrarproveedor/', proveedores, name="proveedores"),
    path('listarusuarios/', listarusuarios, name="listarusuarios"),
    path('cronn/', cron, name="cron"),
    path('log/',log, name="log"),
]
