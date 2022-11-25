from django_cron import CronJobBase, Schedule
import requests
from apps.management.models import ConfigCron, Servicio, Cliente
from datetime import datetime
from django import forms
from apps.management.cron.serializers import SistemaSerializers
from django.conf import settings
import time

class MyCronJob(CronJobBase):


    servicios=['ELE', 'AGU', 'GAS']
    cronconfig = ConfigCron.objects.get(id=1)
    cursor = cronconfig.cursor
    servicio = Servicio.objects.get(id=cursor)
    data = SistemaSerializers(cronconfig)
    #Busca solo a los clientes activos
    clientes = Cliente.objects.filter(is_active=True)
    exec=data.data['hora_exec']
    fecha =data.data['fecha']
    RUN_AT_TIMES = [exec]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'CronProcessDocs' 

    def do(self):
        if self.cronconfig.is_active == True:
            if datetime.now().date()==self.cronconfig.fecha:
                ConfigCron.objects.filter(id=1).update(status = "2")
                for cli in self.clientes:
                    for ser in self.servicios:
                        url4 =  'http://localhost:8000/cron/verificar_status/'
                        cookie = settings.CRON_CREDENCIAL
                        estado = requests.get(url=url4, cookies={'jwt':cookie})
                        con = estado.json()
                        if con['status'] == True:
                            url =  'http://localhost:8000/documentos/search_docs/'
                            cookie = settings.CRON_CREDENCIAL
                            body={
                                'folio': '', 
                                'tipo_servicio': ser,
                                'rut_client': cli.rut_cliente,
                                'rut_receptor': None,
                                'fecha': None
                            }
                            search = requests.post(url=url, json=body, cookies={'jwt':cookie})
                            data = search.json()
                            if search.status_code==200:
                                for bol in data:
                                    ConfigCron.objects.filter(id=1).update(status = "3")
                                    url2 =  'http://localhost:8000/cron/verificar_status/'
                                    cookie = settings.CRON_CREDENCIAL
                                    estado = requests.get(url=url2, cookies={'jwt':cookie})
                                    con = estado.json()
                                    if con['status'] == True:
                                        uidd= bol['uuid']
                                        nomDoc = bol['nomDoc']
                                        rut_emisor = bol['rut_emisor']
                                        rut_cliente = bol['rut_client']
                                        url3 =  'http://localhost:8000/documentos/process_docs/'
                                        body_proc= {'uuid' :uidd , "nomDoc" : nomDoc, "rut_emisor": rut_emisor, "rut_client":rut_cliente}
                                        proc = requests.post(url=url3, json=body_proc, cookies={'jwt':cookie})
                                        time.sleep(5)
                                    else:
                                        ConfigCron.objects.filter(id=1).update(status = "5")
                                        return 'Proceso Detenido'
                        else: 
                            ConfigCron.objects.filter(id=1).update(status = "5")
                            return 'Proceso Detenido'
                ConfigCron.objects.filter(id=1).update(status = "1")
                return 'Proceso Finalizado'
        return 'Proceso en Pausa'

