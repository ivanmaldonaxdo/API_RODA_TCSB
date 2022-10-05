import sys 
# sys.path.append('../OPKM')
# sys.path.append('../AWSTEXTRACT')
from APIOpenKM import OpenKm
from AWS import subir_archivo
import requests
#******PARA EJECUTAR ESTE CODE SE DEBE ESCRIBIR EN EL TERMINAL CMD 'python TestOPKM.py'******
openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
response = openkm.get_docs(_serv='AGU')
# response = openkm.get_docs(_nombre='5293130')
print("")
print("**********SUBIDA DE ARCHIVO A S3**********")
if isinstance(response, list):
    for r in response:
        uuid = r['uuid']
        resp = openkm.get_content_doc(r['uuid'])
        print("**********OBJECT **********")
        print("")
        resultado =  subir_archivo(resp.content,'rodatest-bucket', nomDoc = r['nomDoc'])
else:
    resp = openkm.get_content_doc(response['uuid'])
    resultado = subir_archivo(resp.content,'roda-s3-boto3-bucket', nomDoc = response['nomDoc'])


