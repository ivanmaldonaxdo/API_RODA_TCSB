from django.contrib import admin
from .models import *
from solo.admin import SingletonModelAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from datetime import timedelta
import datetime
from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse


class APILogsAdmin(admin.ModelAdmin):


        def __init__(self, model, admin_site):
            super().__init__(model, admin_site)

        # def added_on_time(self, obj):
        #     return obj.fecha_hora.strftime("%d %b %Y %H:%M:%S")

        # added_on_time.admin_order_field = 'added_on'
        # added_on_time.short_description = 'Added on'

        list_per_page = 20
        list_display = ('id', 'api', 'method', 'status_code', 'fecha_hora',)
        list_filter = ('fecha_hora', 'status_code', 'method',)
        search_fields = ('payload', 'response', 'headers', 'api',)
        readonly_fields = (
            'api',
            'payload', 'method', 'response', 'status_code', 'fecha_hora',
        )
        exclude = ('fecha_hora',)

        date_hierarchy = 'fecha_hora'

        def has_add_permission(self, request, obj=None):
            return False

        def has_change_permission(self, request, obj=None):
            return False



admin.site.register(Sucursal)
admin.site.register(Proveedor)
admin.site.register(Servicio)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Zona)
admin.site.register(Cliente)
admin.site.register(Provincia)
admin.site.register(Sistema, SingletonModelAdmin)
admin.site.register(Documento)
admin.site.register(Contrato_servicio)
admin.site.register(Plantilla)
admin.site.register(LogSistema, APILogsAdmin)


# get_solo will create the item if it does not already exist



