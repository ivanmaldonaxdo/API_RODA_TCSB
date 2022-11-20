
from django.urls import path
from .views import login,homeinfo,processDocs,processed,Cliente,Usuarios

from .views import login,homeinfo,processDocs, test

urlpatterns = [
    path('process/', processDocs, name="process"),
    path('', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo"),
    path('processedDocs/', processed, name="processed"),
    path('Cliente/', Cliente, name="Cliente"),
    path('Usuarios/', Usuarios, name="Usuarios"),
    path('test/', test, name='test')
]
