from django.contrib import admin
from .models import *
from solo.admin import SingletonModelAdmin
# Register your models here.

admin.site.register(Sucursal)
admin.site.register(Proveedor)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Zona)
admin.site.register(Cliente)
admin.site.register(Sistema)
admin.site.register(Documento)




