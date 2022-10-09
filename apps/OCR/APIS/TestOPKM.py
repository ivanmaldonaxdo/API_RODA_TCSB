import sys 
# sys.path.append('../OPKM')
# sys.path.append('../AWSTEXTRACT')
from APIOpenKM import OpenKm
from AWS import subir_archivo
import requests
#******PARA EJECUTAR ESTE CODE SE DEBE ESCRIBIR EN EL TERMINAL CMD 'python TestOPKM.py'******
openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
response = openkm.get_docs(_serv='AGU',_path = '/okm:root/Cobros/76242774-5/1/2020/AGU')
# response = openkm.get_docs(_nombre='5293130')
# print("")
print("**********SUBIDA DE ARCHIVOS A S3**********")
print("")
if isinstance(response, list):
    for r in response:
        uuid = r['uuid']
        print(uuid)
        archivo = openkm.get_content_doc(uuid)
        print(r['nomDoc'])
        # print(resp)
        print(resp.content)
        # resultado =  subir_archivo(archivo.content,'rodatest-bucket', nomDoc = r['nomDoc'])
        print("**********PDF SUBIDO**********")
        print("")
else:
    try:
        archivo = openkm.get_content_doc(response['uuid'])
        print(response['nomDoc'])
        # resultado = subir_archivo(archivocls***")
    except:
        print("ERROR EN SUBIR CONTENIDO")

