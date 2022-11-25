
from django.urls import path
from .views import login,homeinfo,processDocs,processed,test,cron
from .views import login,homeinfo,processDocs,processed,Cliente
from .views import login,homeinfo,processDocs,processed,Cliente,Usuarios,modificarcliente,modificarusuario,listarcliente,listarusuarios, cron

from .views import login,homeinfo,processDocs, test

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
    path('listarusuarios/', listarusuarios, name="listarusuarios"),
    path('cron/', cron, name="cron"),
    path('test/', test, name='test')
]
