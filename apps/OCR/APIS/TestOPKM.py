import sys
# sys.path.append('../OPKM')
# sys.path.append('../AWSTEXTRACT')
from APIOpenKM import OpenKm
from AWS import subir_archivo
import requests
import json
import time

#******PARA EJECUTAR ESTE CODE SE DEBE ESCRIBIR EN EL TERMINAL CMD 'python TestOPKM.py'******
openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
response = openkm.get_docs(_serv='ELE',_path = '/okm:root/Cobros/76242774-5/1/2020/AGU')
# response = openkm.get_docs(_folio='11419589')
print("")
print("**********PROCESAMIENTO DE ARCHIVOS**********")
# print("**********SUBIDA DE ARCHIVOS A S3**********")
if isinstance(response, list):
    for r in response:
        uuid = r['uuid']
        print("*"*153)
        archivo = openkm.get_content_doc(uuid)
        print("")
        print(r['nomDoc'])
        # print(archivo)
        # resultado =  subir_archivo(archivo.content,'rodatest-bucket', nomDoc = r['nomDoc'])
        print("")
        print("PDF SUBIDO")
        print("")
        metadata = openkm.get_metadata(uuid)
        openkm.is_processed_doc(uuid)

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

