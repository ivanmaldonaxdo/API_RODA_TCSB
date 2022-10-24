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
admin.site.register(Provincia)
admin.site.register(Sistema, SingletonModelAdmin)
admin.site.register(Documento)
admin.site.register(Contrato_servicio)

config = Sistema.objects.get()

# get_solo will create the item if it does not already exist
config = Sistema.get_solo()




