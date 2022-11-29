
from django.urls import path
from .views import Sucursales, listarSucursales, login,homeinfo,processDocs,processed,Cliente,Usuarios,modificarcliente,modificarusuario,listarcliente,listarusuarios, cron,log, servicio_cliente

from .views import login,homeinfo,processDocs,test

urlpatterns = [
    path('process/', processDocs, name="process"),
    path('', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo"),
    path('processedDocs/', processed, name="processed"),
    path('automatizacion/', cron, name="cron"),
    path('Cliente/', Cliente, name="Cliente"),
    path('Modificarcliente/', modificarcliente, name="modificarcliente"),
    path('listarcliente/', listarcliente, name="listarcliente"),
    path('registrar-usuarios/', Usuarios, name="Usuarios"),
    path('Modificarusuario/', modificarusuario, name="modificarusuario"),
    path('registrarcontrato/', servicio_cliente, name="registrarcontrato"),
    path('listarusuarios/', listarusuarios, name="listarusuarios"),
    path('cronn/', cron, name="cron"),
    path('log/',log, name="log"),
    path('listarSucursales/', listarSucursales , name="listarSucursales"),
    path('registro-Sucursales/', Sucursales , name="Sucursales"),
    path('test/', test, name='test')
]
