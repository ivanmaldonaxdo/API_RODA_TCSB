from apps.users.models import User
from rest_framework import filters
from rest_framework.response import Response
from apps.permissions import IsOperador, IsAdministrador
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.viewsets import GenericViewSet,ViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from apps.OCR.APIS.APIOpenKM import OpenKm
from apps.OCR.APIS.AWS import subir_archivo
from rest_framework import filters

# from apps.users.authentication import ExpiringTokenAuthentication
class OpenKMViewSet(ViewSet):
    docs = None
    openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
    def format_filtros(self,filtros):
        for k,v in filtros.items():
            if v == "":
                filtros[k] = None
        print("Filtros {} -".format(filtros))
        return filtros
    
    @action(detail=False,methods = ['POST'],url_name="search_docs")
    # @action(detail = False, methods = ['post'])
    def search_docs(self,request):
        filtros = dict(request.data)
        # diction = {}
        filtros = self.format_filtros(filtros)
        print(filtros)
        docs = self.openkm.search_docs(
            _folio = filtros.get('folio'),
            _serv = filtros.get('tipo_servicio'),
            _rutCli = filtros.get('rut_receptor')
        )
        # {"message: Data encontrada"},
        if docs:
            print("HAY ARCHIVOS")
            print("cantidad => {}" .format(len(docs)))
            # print("**********SUBIDA DE ARCHIVOS A S3**********")
            # print("IS LISTA?? -", isinstance(response, list),"- " ,type(response))
            print(docs)
            return Response(data = docs, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)

    #request debe tener el uuid,nomDoc y rutEmisor
    @action(detail=False,methods = ['POST'],url_name="process_docs")
    def process_docs(self,request):
        data = dict(request.data)
        contenido = self.openkm.get_content_doc(
            data.get("uuid")
        ).content
        
        # {"message: Data encontrada"},
        if contenido:
            # print(contenido)
            # data = contenido.decode()
            resultado = subir_archivo(contenido,'rodatest-bucket', nomDoc = data.get('nomDoc'))
            return Response({
                'message':'Documento Procesado',
            }, status=status.HTTP_200_OK,headers=None)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)

        # if isinstance(docs, list):
        #     for r in docs:
        #         uuid = r['uuid']
        #         print("*"*153)
        #         archivo = self.openkm.get_content_doc(uuid)
        #         # resultado =  subir_archivo(archivo.content,'rodatest-bucket', nomDoc = r['nomDoc'])
        #         print("SE HA SUBIDO EL PDF - {}".format(r['nomDoc']))
        #         print("")
        #         metadata = self.openkm.get_metadata(uuid)
        #         print(metadata)
        #         metadata.update({'nomDoc': r['nomDoc']})
        #         metadata_list.append(metadata)
        #         # process_ocr = openkm.set_metadata_processed(uuid,1234)
        #         # print(process_ocr)
        # else:
        #     try:
        #         uuid = docs['uuid']
        #         print("*"*153)
        #         archivo = self.openkm.get_content_doc(uuid)
        #         # resultado = subir_archivo(archivo.content,'rodatest-bucket', nomDoc = docs['nomDoc'])
        #         print("SE HA SUBIDO EL PDF - {}".format(docs['nomDoc']))
        #         print("")
        #         metadata = self.openkm.get_metadata(uuid)
        #         metadata.update({'nomDoc': docs['nomDoc']})
        #         print(metadata)
        #         metadata_list.append(metadata)
        #         # metadata_list = metadata
        #         # process_ocr = openkm.set_metadata_processed(uuid,1234)

        #     except:
        #         print("ERROR EN SUBIR/PROCESAR ARCHIVO A S3 AWS")

   
   
   
    # def list(self,request):
    #     print(self.docs)
    #     serializer = self.docs
    #     return Response(serializer.data, status=status.HTTP_200_OK)
 
    # json_tables =  {"Tablas" : ["Tabla_1","Tabla_2"]}  