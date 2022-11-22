from django_cron import CronJobBase, Schedule
import requests
from apps.management.models import ConfigCron
from datetime import datetime
from django import forms
from apps.management.cron.serializers import SistemaSerializers
from django.conf import settings
from django.urls import reverse

class MyCronJob(CronJobBase):
    cronconfig=ConfigCron.objects.get(id=1)
    cursor = cronconfig.cursor

    servicios = ['AGU','ELE','GAS']

    data=SistemaSerializers(cronconfig)
    luz=data.data['hora_luz']
    agua=data.data['hora_agua']
    gas=data.data['hora_gas']
    #RUN_EVERY_MINS = 3
    RUN_AT_TIMES = [luz]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    #schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CronProcessDocs'    # a unique code

    def do(self):
        url =  'http://localhost:8000/documentos/search_docs/'
        cookie = settings.CRON_CREDENCIAL
        body={'folio': '', 'tipo_servicio': 'GAS', 'rut_receptor': None}
        search = requests.post(url=url, json=body, cookies={'jwt':cookie})
        data = search.json()
        for bol in data:
            uidd= bol['uuid']
            nomDoc = bol['nomDoc']
            rut_emisor = bol['rut_emisor']
            url =  'http://localhost:8000/documentos/process_docs/'
            body_proc= {'uuid' :uidd , "nomDoc" : nomDoc, "rut_emisor": rut_emisor}
            proc = requests.post(url=url, json=body_proc, cookies={'jwt':cookie})
        if self.cronconfig.cursor<2:
            ConfigCron.objects.filter(id=1).update(cursor = self.cursor+1)
        elif self.cursor == 2:
            ConfigCron.objects.filter(id=1).update(cursor = 0)
        return str(data)

