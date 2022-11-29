
from cgi import test
from django.urls import path
from .views import Sucursales, listarSucursales, listarplantillas, login,homeinfo, modificarSucursales, plantillas,processDocs,processed,Cliente,Usuarios,modificarcliente,modificarusuario,listarcliente,listarusuarios, cron,log
from .views import Sucursales, listarSucursales, login,homeinfo,processDocs,processed,Cliente,Usuarios,modificarcliente,modificarusuario,listarcliente,listarusuarios, cron,log, servicio_cliente
from .views import *

# from .views import login,homeinfo,processDocs

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
    path('registrarproveedor/', proveedores, name="proveedores"),
    path('listarusuarios/', listarusuarios, name="listarusuarios"),
    path('cronn/', cron, name="cron"),
    path('log/',log, name="log"),
    path('listarSucursales/', listarSucursales , name="listarSucursales"),
    path('registro-Sucursales/', Sucursales , name="Sucursales"),
    path('modificarSucursales/', modificarSucursales , name="modificarSucursales"),
    path('listarplantillas/', listarplantillas , name="listarlistarplantillas"),
    path('registrarplantilla/', plantillas , name="registrarplantilla"),
    path('modificarplantilla/', modificarplantilla , name="modificarplantilla"),
    
    path('listarproveedores/', listarproveedores , name="listarproveedores"),
    path('registrarproveedores/', registrarproveedores , name="registrarproveedores"),
    path('test/', test, name='test'),
    path('get_client/', get_client , name="get_client"),
]
