from django.contrib import admin

from apps.management.models import Sistema, Cliente
from .models import User, Rol

from rest_framework.authtoken.models import Token

# Register your models here.

admin.site.register(User)
admin.site.register(Rol)
admin.site.register(Sistema)
admin.site.register(Cliente)