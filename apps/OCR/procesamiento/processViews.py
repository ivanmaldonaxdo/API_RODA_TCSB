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
from apps.management.models import Plantilla,Cliente,Sucursal,Documento,Sistema,Contrato_servicio
from django.db.models import Q
import json
import os
import csv
from django.conf import settings# from django.core.files.storage
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots
import sys
from apps.permissions import  *

# from apps.users.authentication import ExpiringTokenAuthentication
class OpenKMViewSet(ViewSet):
    # permission_classes = (IsAdministrador,IsOperador,)
    # permission_classes = [IsAdministrador,IsOperador]

    docs = None
    openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
    def format_filtros(self,filtros):
        for k,v in filtros.items():
            if k not in ['dia_doc','anio_doc','mes_doc']:
                if v == "":
                    filtros[k] = None
        print("Filtros {} -".format(filtros))
        return filtros

    @action(detail=False,methods = ['POST'],url_name="search_docs")
    # @action(detail = False, methods = ['post'])
    def search_docs(self,request):
        filtros = dict(request.data)
        # diction = {}
        openkm = self.openkm_creds()
        # print("OPKM OBJECT ", openkm.auth_creds.password)
        filtros = self.format_filtros(filtros)
        print("Filtros Search Docs")
        print(filtros)
        anio = None
        mes = None
        dia = None
        try:
            print(str(filtros.get("fecha")).split("-"))
            anio,mes,dia = str(filtros.get("fecha")).split("-")
        except:
            print("No Fechita")
        docs = openkm.search_docs(
            _folio = filtros.get('folio'),
            _serv = filtros.get('tipo_servicio'),
            _rutCli = filtros.get('rut_client'),
            _rutReceptor = filtros.get('rut_receptor'),
            dia = dia,
            mes = mes,
            anio = anio 
            # dia = filtros.get('dia'),
            # mes = filtros.get('mes'),
            # anio = filtros.get('anio')

            
        )
        # {"message: Data encontrada"},
        if docs:
            print("HAY ARCHIVOS")
            return Response(data = docs, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)

#region Description
    #request debe tener el uuid,nomDoc y rutEmisor
    @action(detail=False,methods = ['POST'],url_name="process_docs")
    def process_docs(self,request):
        try:
            openkm = self.openkm_creds()
            data = dict(request.data)
            contenido = openkm.get_content_doc(
                data.get("uuid")
            ).content
            print(type(openkm.get_content_doc(data.get("uuid")).content))
            try:
                rut_client = data.get('rut_client')

                # rut_client = data.get('rut_client')
                cliente = Cliente.objects.get(rut_cliente=data.get('rut_client'))
                if cliente.is_active:
                    ######################## SUBIDA DE ARCHIVO EN S3 AWS ##############################
                    resultado = subir_archivo(contenido,'rodatest-bucket', nomDoc = data.get('nomDoc'))

                    ######################## CONSULTA DE PLANTILLAS EN BD #############################
                    print(data.get('rut_emisor'))
                    with connections['default'].cursor() as cursor:##conexion default a la bd
                        cursor.execute('''select * from v_plantillas where rut_proveedor = %s''',[data.get('rut_emisor')])
                        plantilla = cursor.fetchall()
                    queries_file,tables_file = plantilla[0][2],plantilla[0][3]
                    print("Queries file: ", queries_file, " - Tables_config: ", tables_file ) 
                    queries_file_path = os.path.join('media',queries_file)
                    query_doc = 'media'+ '/' + queries_file
                    table_doc = 'media'+ '/' + tables_file
                    print(type(table_doc))

                    ######################## EXTRACCION DE DATA EN BOTO 3 ##############################
                    extracted_data = extraccionOCR('rodatest-bucket',query=query_doc,tables = table_doc, nomDoc = data.get('nomDoc'))
                    metadata = openkm.get_metadata(data.get("uuid"))

                    docName = str(data.get('nomDoc')).replace('.pdf', '')
                    archivo  = ( docName + '.json')

                    ######## RUT DE CLIENTE
                    # rut_cliente = str(extracted_data.get('RUT_CLIENTE')).replace(":", "").strip()
                    # rut_cliente = format_rut_without_dots(rut_cliente)
                    numero_cli = extracted_data.get("Nro CLIENTE")

                    ######################## OBTENCION DE CONTENIDO JSON PARA SUBIDA ###################
                    read = json.dumps(extracted_data, indent = 4)
                    contenido = ContentFile(read.encode('utf-8'))
                    contrato_serv = Contrato_servicio.objects.get(num_cliente = numero_cli)
                    # id_contrat = contrato_serv.sucursal.id
                    # print(id_contrat)
                    ######################## SUBIDA DE JSON ESTRUCTURADOS EN BD ########################
                    doc = Documento.objects.create(
                        nom_doc = docName,
                        folio =  metadata.get('folio'),
                        contrato_servicio = contrato_serv,
                        procesado = True                     
                    )
                    subido = doc.documento.save(archivo,contenido)
                    id_doc = doc.id
                    # print(id_doc)
                    # self.openkm.set_metadata_processed(data.get("uuid"), extracted_data.get('JOB_ID'))
                    return Response({
                        'message':'Documento Procesado','numCli':numero_cli,'uuid':data.get("uuid"),"DocID":id_doc

                        }, status=status.HTTP_200_OK,headers=None)
                    
                    # folio,rutCli = metadata.get("folio"), metadata.get("rut")
                else:
                    return Response({

                        'message':'Documento No Procesado, cliente con rut {} se encuentra desactivado en el sistema' .format(rut_client)
                    }, status=status.HTTP_401_UNAUTHORIZED,headers=None)
                    
            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno

                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)
                print(e)
                error = ""
                rut_proveedor = data.get('rut_emisor')
                if str(e) == "list index out of range":
                    error = "No hay plantillas relacionadas a proveedor con rut {}" .format(rut_proveedor)
                elif str(e) =="Cliente matching query does not exist.":
                    error = "No exite algun cliente relacionado al rut {}" .format(rut_client)
                else:
                    error = str(e)
                print(error)
                return Response({
                    'message':'Documento No Procesado','Error':error, 'uuid':data.get('uuid')
                    }, status=status.HTTP_409_CONFLICT,headers=None)
    
        except Exception as e:
            print(e)            
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)

#region Description
    @action(detail=False,methods = ['GET'],url_name = "probar_creds") 
    def probar_creds(self,request):
        credenciales = self.credenciales()
        # openkm_cred = credenciales.
        print("")
        print("credenciales  ",credenciales)

        # print("openkm ",openkm_cred)
        # print()
        # sis.get("")
        return Response({
                'message':'Creds'
            }, status=status.HTTP_200_OK,headers=None)



    @action(detail=False,methods = ['POST'],url_name="process_by_servicio")
    def process_by_servicio (self,request):
        filtros = dict(request.data)
        # diction = {}
        openkm = self.openkm_creds()
        # print("OPKM OBJECT ", openkm.auth_creds.password)
        docs = openkm.search_docs(
            _serv = filtros.get('tipo_servicio')
        )
        # {"message: Data encontrada"},
        if docs:
            print("HAY ARCHIVOS")
            return Response(data = docs, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)

    ######## ESTA FUNCION EXTRAE LAS CREDENCIALES DE OPENKM Y ADEMAS INSTANCIA A LA CLASE APIOpenKM   
    def openkm_creds(self):
        creds = self.credenciales()
        opk = creds.get("openkm")
        openkm = OpenKm(
            opk.get("username"), 
            opk.get("password"), 
            opk.get("end_point_base")
        )
        return openkm
    ######### ESTA FUNCION SE ENCARGA DE LEER EL ARCHIVO DE CREDENCIALES DE SISTEMA
    def credenciales(self):
        sistema = Sistema.objects.all().first()
        cantidad = Sistema.objects.count()
        sis = model_to_dict(sistema)
        sistema_file ="media" + "/" + str(sis.get("credencial"))
        # print(sistema_file)
        # sistema = 
        # print("",cantidad, " - " ,sis)
        # Opening JSON file
        json_creds = dict()

        ######### LECTURA DE ARCHIVO ##########
        with open(sistema_file) as json_file:
            data = json.load(json_file)
            # print(data)
            json_creds.update(data)
        
        creds = dict()
        ########## FORMATEANDO DE LISTA CREDENCIALES A UN DICCIONARIO PARA ACCEDER A CADA CREDENCIAL POR SU NOMBRE
        for cred in json_creds.get("credenciales"):
            creds.update(cred)
        # openkm_sis, aws_sis = creds.get("openkm"), creds.get("aws")
        # print(creds)
        return creds

    def validar_rut(self,value):
        rut_validado = is_valid_rut(value)
        if rut_validado == True:
            return value
        else:
            print("El rut no es valido")

    #REFERENCIAS https://realpython.com/python-csv/