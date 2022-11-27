import logging
from django.utils.deprecation import MiddlewareMixin
import json
from django.urls import resolve
from apps.management.models import LogSistema, Documento
from apps.OCR.APIS.APIOpenKM import OpenKm
from apps.OCR.procesamiento.processViews import OpenKMViewSet 
procesamiento = OpenKMViewSet()


class LogRestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        
        url_name = resolve(request.path_info).url_name
        namespace = resolve(request.path_info).namespace

        if namespace == 'admin':
                return self.get_response(request)
        if url_name == 'logout':
                return self.get_response(request)
        if url_name == 'cron-verificar-status':
                return self.get_response(request)
        if url_name == 'rol':
                return self.get_response(request)
        
        
        request_data = ''
        try:
            request_data = json.loads(request.body) if request.body else ''
        except:
            pass
            
        response = self.get_response(request)
        
        if request.user.id is not None:
            user = request.user.id
        else:
            user = 0
        method=request.method
        api = request.build_absolute_uri()
        
        if response.get('content-type') in ('application/json', 'application/vnd.api+json',):
                if getattr(response, 'streaming', False):
                    response_body = '** Streaming **'
                else:
                    if type(response.content) == bytes:
                        response_body = json.loads(response.content.decode())
                    else:
                        response_body = json.loads(response.content)
                data = dict(
                    api=api,
                    id_user=user,
                    payload=request_data,
                    cliente= 'No aplica',
                    method=method,
                    response=response_body,
                    status_code=response.status_code,
                )
                if url_name == 'search_docs-process_docs' and data['status_code'] == 200:
                    document = Documento.objects.get(id=response_body["DocID"])
                    sucursal = document.contrato_servicio.sucursal
                    # sucursal = contrato.sucursal.rut_sucursal
                    data['cliente'] = sucursal.rut_sucursal

                # create instance of model
                m = LogSistema(**data)
                # don't forget to save to database!
                m.save()
                if url_name == 'search_docs-process_docs' and m.status_code == 200:
                    openkm = procesamiento.openkm_creds()
                    # openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
                    uuid= response_body["uuid"]
                    codigo = m.id
                    openkm.set_metadata_processed(uuid,codigo)
                if url_name == 'search_docs-process_docs' and m.status_code != 200:
                    openkm = procesamiento.openkm_creds()
                    uuid= response_body["uuid"]
                    codigo = str(m.id) + " TAG ERROR"
                    openkm.set_metadata_processed(uuid,codigo)
        else:
            return response

        return response