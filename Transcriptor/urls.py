"""Transcriptor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users.views import authUser, Logout
from django.conf.urls.static import static
from django.conf import settings

#falta agregar al path
#path('procesoauto/', include('apps.OCR.automatico.routers')),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth-user/', authUser.as_view(), name='auth-user'),
    path('logout/', Logout.as_view(), name='logout'),
    path('usuarios/', include('apps.users.usuarios.routers')),
    path('clientes/', include('apps.management.clientes.routers')),
    path('proveedores/', include('apps.management.proveedor.routers')),
    path('procesoauto/', include('apps.OCR.automatico.routers')),
    path('sucursales/', include('apps.management.sucursales.routers')),
    path('plantillas/', include('apps.management.plantilla.routers')),
    path('documentos/',include('apps.OCR.procesamiento.routers')),
    path('sistema/',include('apps.management.sistema.routers')),
    path('procesados/',include('apps.management.procesados.routers')),
    path('logs',include('apps.management.Logs.routers')),
    path('', include('apps.frontend.urls'))
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)