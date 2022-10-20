from django.contrib import admin
from .models import User, Rol
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin




TokenAdmin.raw_id_fields = ['user']
admin.site.register(User)
admin.site.register(Rol)
admin.site.unregister(Group)
