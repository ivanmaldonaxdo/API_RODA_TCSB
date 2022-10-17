from django.contrib import admin
from .models import User, Rol
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

# Register your models here.




admin.site.register(User)
admin.site.register(Rol)
admin.site.unregister(Group)
