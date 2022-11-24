from django_cron import CronJobBase, Schedule
import requests
from apps.management.models import ConfigCron, Servicio
from datetime import datetime
from django import forms
from apps.management.cron.serializers import SistemaSerializers
from django.conf import settings
import time

class MyCronJob(CronJobBase):
    cronconfig=ConfigCron.objects.get(id=1)
    cursor = cronconfig.cursor
    servicio = Servicio.objects.get(id=cursor)
    data=SistemaSerializers(cronconfig)
    exec=data.data['hora_exec']
    #RUN_EVERY_MINS = 5
    RUN_AT_TIMES = [exec]
    #schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
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
            #     url2 =  'http://localhost:8000/cron/verificar_status/'
            #     cookie = settings.CRON_CREDENCIAL
            #     estado = requests.get(url=url2, cookies={'jwt':cookie})
            #     con = estado.json()
            #     if con['status'] == True:
            #         uidd= bol['uuid']
            #         nomDoc = bol['nomDoc']
            #         rut_emisor = bol['rut_emisor']
            #         rut_cliente = bol['rut_client']
            #         url3 =  'http://localhost:8000/documentos/process_docs/'
            #         body_proc= {'uuid' :uidd , "nomDoc" : nomDoc, "rut_emisor": rut_emisor, "rut_client":rut_cliente}
            #         proc = requests.post(url=url3, json=body_proc, cookies={'jwt':cookie})
            #         time.sleep(5)
            #     else:
            #         return 'Proceso Pausado'
            ConfigCron.objects.filter(id=1).update(status = 'Finalizando')
            if self.cronconfig.cursor<2:
                ConfigCron.objects.filter(id=1).update(cursor = self.cursor+1)
            elif self.cursor == 2:
                ConfigCron.objects.filter(id=1).update(cursor = 0)
            ConfigCron.objects.filter(id=1).update(status = 'Terminado o En espera')
            return 'Proceso Finalizado'
        return 'Proceso en Pausa'

