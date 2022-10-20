from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse, response
from OCR.APIS.APIOpenKM import OpenKm
import sys
import requests
import json
import time

#funcion CRON de prueba
def dicehola(request):
    
    return HttpResponse("nuevamente provando cron")


#solo usaremos esta funcion para descargar y probar openkm con 1 pdf o un conjungo
#se probara en postman ingresar un 1 o 0 para la ejecucion del proceso cada ciertas horas/dias

def openkmauto(auto):
    
    if auto == 1 :
       
        openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
          # response = openkm.get_docs(_serv='ELE',_rutCli = '76242774-5' )
    response = openkm.get_docs(_folio='11419589')
        # response = openkm.get_docs(_serv='ELE')

    response = openkm.get_docs()

    print("")
    print("PROCESAMIENTO DE ARCHIVOS")
    # print("**********SUBIDA DE ARCHIVOS A S3**********")
    # print("IS LISTA?? -", isinstance(response, list),"- " ,type(response))
    if isinstance(response, list):
        for r in response:
            uuid = r['uuid']
            print("*"*153)
            archivo = openkm.get_content_doc(uuid)
            # print(archivo)
            # resultado =  subir_archivo(archivo.content,'rodatest-bucket', nomDoc = r['nomDoc'])
            print("SE HA SUBIDO EL PDF - {}".format(r['nomDoc']))
            print("")
            metadata = openkm.get_metadata(uuid)
            # print(meta)
            # openkm.is_processed_doc(uuid)
            print("JSON PROPS => {}" .format(json.dumps(metadata,indent = 2)))

            # print(metadata.get('folio'))
        
    else:
        try:
            archivo = openkm.get_content_doc(response['uuid'])
            print(response['nomDoc'])
            # resultado = subir_archivo(archivo.content,'rodatest-bucket', nomDoc = response['nomDoc'])
            print("")
            print("PDF SUBIDO")
            print("")
            print("METADATA")
            metadata = openkm.get_metadata(response['uuid'])
        except:
            print("ERROR EN SUBIR/PROCESAR ARCHIVO A S3 AWS")

                                                                                                                                                                        
            print("cada 2 mit")
        
        else:
                print("no se ejecuta")
                return HttpResponse("no se ejecutara el proceso automatico en un dia")

#solo para probar CRON y demases
openkmauto(0)

#crearemos una funcion solo para descargra archivos de openKM

def descopenKM():
    
    print('ses')


