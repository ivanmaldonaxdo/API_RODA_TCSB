import array
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.viewsets import GenericViewSet,ViewSet
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from apps.OCR.APIS.APIOpenKM import OpenKm
from apps.OCR.APIS.AWS import subir_archivo,extraccionOCR
from rest_framework import filters
from django.db import connections
from apps.management.models import Plantilla,Cliente,Sucursal,Documento,Sistema
from django.db.models import Q
import json
import os
import csv
from django.conf import settings# from django.core.files.storage
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots
from datetime import datetime

class procesoautomatico(ViewSet):
    docs = None
    openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
    def format_filtros(self,filtros):
        for k,v in filtros.items():
            if v == "":
                filtros[k] = None
        print("Filtros {} -".format(filtros))
        return filtros


    @action(detail=False,methods = ['POST'],url_name="pruebausu")
    def pruebausu(self,request):
        url = 'http://3.239.229.60/clientes/'
        x = request.get(url)
        

    @action(detail=False,methods = ['POST'],url_name="procesook")
    def procesook(self,request):

        #(falta mejorar esta funcion para filtrar por usuarios/servicio/rutreceptor)
        #pensar mejor por parametros y folio especifico
        #si este ya fue procesado se devuelve la hora y todos sus datos de procesamiento

        #inicio con este ciclo for filtramos por usuario activo para cada cliente de roda
        #obtenemos todos los clientes de la BD
        
        #dentro del proceso filtramos por servicio
        #creamos un models en cliente  que devuelva el servicio contratado(agua,luz,gas)
        

        #filtramos por cron activo , es decir todo el proceso automatico
        
        #http://3.239.229.60/documentos/process_docs/' procesa archivos
        #http://3.239.229.60/documentos/search_docs/'; los busca
        #const url = 'http://3.239.229.60/procesados/' busca procesados
        
        cron_activo = cron.objects.get(id=2)

        if cron_activo.is_active == True:
                    cli2 = Cliente.objects.all()
                    for c in cli2:
                        if c.is_active:
                            #aqui funciones para detener por dia/ hora
                            #se podra realizar el proceso pasandole el rut del cliente por parametros
                            #REALIZAR FUNCIONES POR REQUEST
                            
                            filtros = dict(request.data)
                            openkm = self.openkm_creds()
                            filtros = self.format_filtros(filtros)
                            docs = openkm.search_docs(
                                _folio = filtros.get('folio'),
                                _serv = filtros.get('tipo_servicio'), 
                                _rutCli = filtros.get('rut_receptor')
                            )
                            if docs:
                                print("HAY ARCHIVOS")
                                data = docs
                                data = dict(request.data)
                                contenido = self.openkm.get_content_doc(data.get("uuid")).content
                                try:
                                    ######################## SUBIDA DE ARCHIVO EN S3 AWS ##############################
                                    resultado = subir_archivo(contenido,'rodatest-bucket', nomDoc = data.get('nomDoc'))
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
                                    metadata = self.openkm.get_metadata(data.get("uuid"))

                                    ######################## SUBIDA DE JSON ESTRUCTURADOS EN BD ########################
                                    docName = str(data.get('nomDoc')).replace('.pdf', '')
                                    archivo  = ( docName + '.json')
                                    read = json.dumps(extracted_data, indent = 4)
                                    contenido = ContentFile(read.encode('utf-8'))
                                    rut_cliente = str(extracted_data.get('RUT_CLIENTE')).replace(":", "").strip()
                                    rut_cliente = format_rut_without_dots(rut_cliente)
                                    doc = Documento.objects.create(
                                        nom_doc = docName,
                                        folio =  metadata.get('folio'),
                                        sucursal = Sucursal.objects.get(rut_sucursal = rut_cliente), 
                                        procesado = True                     
                                    )
                                    subido = doc.documento.save(archivo,contenido)
                                    id_doc = doc.id
                                    x = datetime.now()
                                    dia = x.day
                                    hora = x.hour
                                    min = x.minute
                                    hora= repr(dia)+'/ '+repr(hora)+' '+repr(min) 
                                    #proceso_final = c.nom_cli + id_doc + doc.docName + doc.folio + hora_actual2
                                    return Response({'message':'Documento Procesado','DodcID':id_doc,
                                                        'uuid':data.get("uuid"),
                                                        'dia/ hora del proceso':hora,
                                                    }, status=status.HTTP_200_OK,headers=None)
                                
                                except Exception as e:
                                    #si el documento ya fue procesado  se debe mostrar igual
                                        print(e)
                                        print(c.nom_cli +' '+'este usuario esta activo') 
                                        return Response({'message':'Documento no Procesado',}, status= status.HTTP_404_NOT_FOUND)
                                        #aqui respuesta del for 

                            #el proceso automatico de por si trae los documentos sin procesar       
                            #se debera modificar este codigo 
                            else:
                                #sino esta el documento se muestra
                                #por folio ya que por servicio no va al caso
                                filtros = dict(request.data)
                                folio = filtros.get('folio')
                                return Response({'message':'Documento no encontrado',
                                                'folio':folio}
                                                , status= status.HTTP_404_NOT_FOUND)
                    else:
                        print(c.nom_cli)
                        x = datetime.now()
                        dia = x.day
                        hora = x.hour
                        min = x.minute
                        hora= repr(dia)+'/ '+repr(hora)+' '+repr(min)
                        print(hora)
                        print(c.nom_cli)
                        return Response({'message':'proceso desactivado por servicio impago',
                                            'dia/ hora del proceso':hora,
                                            'cliente': c.nom_cli}
                                            ,status= status.HTTP_404_NOT_FOUND)
                     
        else:
            x = datetime.now()
            dia = x.day
            hora = x.hour
            min = x.minute
            hora= repr(dia)+'/ '+repr(hora)+' '+repr(min)
            return Response({'message':'Cron esta desactivado',
                                'dia/ hora ':hora,}
                                ,status= status.HTTP_404_NOT_FOUND)


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
        print(creds)
        return creds

    def validar_rut(self,value):
        rut_validado = is_valid_rut(value)
        if rut_validado == True:
            return value
        else:
            print("El rut no es valido")

    #REFERENCIAS https://realpython.com/python-csv/

  
        
         

















