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
from apps.users.views import Login
from apps.OCR import cron
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='Login'),
    path('usuarios/', include('apps.users.usuarios.routers')),
    path('clientes/', include('apps.management.clientes.routers')),
    path('proveedores/', include('apps.management.proveedor.routers')),
<<<<<<< HEAD
    path('cron/', cron.dicehola),
    path('', include('apps.frontend.urls'))
=======
    path('sucursales/', include('apps.management.sucursales.routers')),
    path('documentos/',include('apps.OCR.procesamiento.routers')),
    path('cron/', cron.dicehola)
>>>>>>> f26b3d64ef28272a714da7210cc0cb37d5850d25
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)