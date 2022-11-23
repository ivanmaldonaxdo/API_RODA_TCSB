from django_cron import CronJobBase, Schedule
import requests
from apps.management.models import ConfigCron, Servicio
from datetime import datetime
from django import forms
from apps.management.cron.serializers import SistemaSerializers
from django.conf import settings

class MyCronJob(CronJobBase):
    cronconfig=ConfigCron.objects.get(id=1)
    cursor = cronconfig.cursor
    servicio = Servicio.objects.get(id=cursor)

    data=SistemaSerializers(cronconfig)
    luz=data.data['hora_luz']
    agua=data.data['hora_agua']
    gas=data.data['hora_gas']
    RUN_EVERY_MINS = 1
    #RUN_AT_TIMES = ['05:00',]
    #schedule = Schedule(run_at_times=RUN_AT_TIMES)
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CronProcessDocs'    # a unique code

    def do(self):
        if self.cronconfig.is_active == True:
            url =  'http://localhost:8000/documentos/search_docs/'
            cookie = settings.CRON_CREDENCIAL
            body={'folio': '', 'tipo_servicio': self.servicio.servicio, 'rut_receptor': None}
            ConfigCron.objects.filter(id=1).update(status = 'Buscando Informacion')
            search = requests.post(url=url, json=body, cookies={'jwt':cookie})
            data = search.json()
            ConfigCron.objects.filter(id=1).update(status = 'Procesando documentos')
            # for bol in data:
            #     uidd= bol['uuid']
            #     nomDoc = bol['nomDoc']
            #     rut_emisor = bol['rut_emisor']
            #     url =  'http://localhost:8000/documentos/process_docs/'
            #     body_proc= {'uuid' :uidd , "nomDoc" : nomDoc, "rut_emisor": rut_emisor}
            #     proc = requests.post(url=url, json=body_proc, cookies={'jwt':cookie})
            ConfigCron.objects.filter(id=1).update(status = 'Finalizando')
            if self.cronconfig.cursor<3:
                ConfigCron.objects.filter(id=1).update(cursor = self.cursor+1)
            elif self.cursor == 3:
                ConfigCron.objects.filter(id=1).update(cursor = 1)
            ConfigCron.objects.filter(id=1).update(status = 'Terminado o En espera')
            return str(data)
        else:
            return 'El proceso esta detendido indefinidamente'

