from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.viewsets import GenericViewSet,ViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from apps.OCR.APIS.APIOpenKM import OpenKm
from apps.OCR.APIS.AWS import subir_archivo,extraccionOCR
from rest_framework import filters
from django.db import connections
from apps.management.models import Plantilla,Cliente,Sucursal,Documento
from django.db.models import Q
import json
import os
import csv
from django.conf import settings# from django.core.files.storage
from django.core.files.base import ContentFile

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
        try:
            data = dict(request.data)
            contenido = self.openkm.get_content_doc(
                data.get("uuid")
            ).content
            
            # {"message: Data encontrada"},
            if contenido:
                # print(contenido)
                # data = contenido.decode()
                resultado = subir_archivo(contenido,'rodatest-bucket', nomDoc = data.get('nomDoc'))
                with connections['default'].cursor() as cursor:##conexion default a la bd
                    cursor.execute('''select * from v_plantillas where rut_proveedor = %s''',[data.get('rut_emisor')])
                    plantilla = cursor.fetchall()
                try:
                    queries_file,tables_file = plantilla[0][2],plantilla[0][3]
                    print("Queries file: ", queries_file, " - Tables_config: ", tables_file ) 
                    queries_file_path = os.path.join('media',queries_file)
                    query_doc = 'media'+ '/' + queries_file
                    table_doc = 'media'+ '/' + tables_file
                    print(type(table_doc))
                    extracted_data = extraccionOCR('rodatest-bucket',query=query_doc,tables = table_doc, nomDoc = data.get('nomDoc'))
                    metadata = self.openkm.get_metadata(data.get("uuid"))
                    docName = str(data.get('nomDoc')).replace('.pdf', '')
                    archivo  = ( docName + '.json')
                    read = json.dumps(extracted_data, indent = 4)
                    contenido = ""
                    try:
                        # print(read)
                        contenido = ContentFile(read.encode('utf-8'))
                        doc = Documento.objects.create(
                            nom_doc = docName,
                            folio =  metadata.get('folio'),
                            sucursal = Sucursal(id = 1), 
                            procesado = True                     
                        )
                        subido = doc.documento.save(archivo,contenido)
                    except Exception as e: # work on python 3.x
                        print(e)
                    # print("txt xdddd  ",txt)
                    # print(metadata)
                    try:
                        sucursal_id = Cliente().objects.select_related('sucursal')
                    except:
                        print("Sucursal No es posible buscar")


                    # folio,rutCli = metadata.get("folio"), metadata.get("rut")

                    return Response({
                        'message':'Documento Procesado',
                    }, status=status.HTTP_200_OK,headers=None)
                except:
                    print("Unable to Acces a queries config")
                    return Response({
                        'message':'Documento No Procesado',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,headers=None)
            else:   
                return Response({
                    'message':'La busqueda no coincide con ningun documento',
                }, status= status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)
            
    # def createJSON(nomDoc):
    #     return ""
    # def list(self,request):
    #     print(self.docs)
    #     serializer = self.docs
    #     return Response(serializer.data, status=status.HTTP_200_OK)
 
    # json_tables =  {"Tablas" : ["Tabla_1","Tabla_2"]}  


    #REFERENCIAS https://realpython.com/python-csv/