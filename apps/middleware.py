import logging
from django.utils.deprecation import MiddlewareMixin
import json
from django.urls import resolve
from apps.management.models import LogSistema
from apps.OCR.APIS.APIOpenKM import OpenKm
class LogRestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        
        url_name = resolve(request.path_info).url_name
        namespace = resolve(request.path_info).namespace
        if namespace == 'admin':
                return self.get_response(request)

        request_data = ''
        try:
            request_data = json.loads(request.body) if request.body else ''
        except:
            pass
            
        response = self.get_response(request)
        user = request.user.id
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
                    method=method,
                    response=response_body,
                    status_code=response.status_code,
                
                )
                # create instance of model
                m = LogSistema(**data)
                # don't forget to save to database!
                m.save()
                if url_name == 'search_docs-process_docs' and m.status_code == 200:
                    openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
                    uuid= response_body["uuid"]
                    codigo = m.id
                    openkm.set_metadata_processed(uuid,codigo)
                    print('metadata actualizada')

        else:
            return response

        return response