import sys
# sys.path.append('../OPKM')
# sys.path.append('../AWSTEXTRACT')
from APIOpenKM import OpenKm
from AWS import subir_archivo, textract
import requests
import json
import time

#******PARA EJECUTAR ESTE CODE SE DEBE ESCRIBIR EN EL TERMINAL CMD 'python TestOPKM.py'******
openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
# response = openkm.search_docs(_serv='ELE',_rutCli = '76242774-5' )
response = openkm.search_docs(_folio='11419589')
# response = openkm.search_docs(_serv='ELE')

print("")
print("PROCESAMIENTO DE ARCHIVOS")
# print("**********SUBIDA DE ARCHIVOS A S3**********")
# print("IS LISTA?? -", isinstance(response, list),"- " ,type(response))
if isinstance(response, list):
    for r in response:
        uuid = r['uuid']
        print("*"*153)
        archivo = openkm.get_content_doc(uuid)
        resultado =  subir_archivo(archivo.content,'rodatest-bucket', nomDoc = r['nomDoc'])
        print("SE HA SUBIDO EL PDF - {}".format(r['nomDoc']))
        print("")
        metadata = openkm.get_metadata(uuid)
        # print(metadata)
        textract('rodatest-bucket', nomDoc = r['nomDoc'])
        # print("RUT EMISOR: {} " .format(metadata.get("rut_emisor")))
        # print("Se ha procesado ??? {}" .format(openkm.is_processed_doc(uuid)))
        # print("Tiene grupo de propiedad ??? {}" .format(openkm.is_in_group_metadata(uuid)))

        # print(meta)
        # openkm.is_processed_doc(uuid)
        # print("JSON PROPS => {}" .format(json.dumps(metadata,indent = 2)))

        # print(metadata.get('folio'))

else:
    try:
        uuid = response['uuid']
        print("*"*153)
        archivo = openkm.get_content_doc(uuid)
        resultado = subir_archivo(archivo.content,'rodatest-bucket', nomDoc = response['nomDoc'])
        print("SE HA SUBIDO EL PDF - {}".format(response['nomDoc']))
        print("")
        metadata = openkm.get_metadata(uuid)
        # print(metadata)
        textract('rodatest-bucket', nomDoc = response['nomDoc'])
        # process_ocr = openkm.set_metadata_processed(uuid,1234)
        # print(process_ocr)
        # print("RUT EMISOR: {} " .format(metadata.get("rut_emisor")))
        # print("Se ha procesado ??? {}" .format(openkm.is_processed_doc(uuid)))
        # print("Tiene grupo de propiedad ??? {}" .format(openkm.is_in_group_metadata(uuid)))
        # print(metadata.get('folio'))

    except:
        print("ERROR EN SUBIR/PROCESAR ARCHIVO A S3 AWS")

