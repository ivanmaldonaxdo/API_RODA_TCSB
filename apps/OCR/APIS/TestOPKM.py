import sys 
# sys.path.append('../OPKM')
# sys.path.append('../AWSTEXTRACT')
from APIOpenKM import OpenKm
from AWS import subir_archivo
import requests
#******PARA EJECUTAR ESTE CODE SE DEBE ESCRIBIR EN EL TERMINAL CMD 'python TestOPKM.py'******
openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
response = openkm.get_docs(_folio = '5293130', _serv='ELE',_path = '/okm:root/Cobros/76242774-5/1/2020/AGU')
# response = openkm.get_docs(_nombre='5293130')
# print("")
print("**********SUBIDA DE ARCHIVOS A S3**********")
print("")
if isinstance(response, list):
    for r in response:
        uuid = r['uuid']
        resp = openkm.get_content_doc(r['uuid'])
        print(r['nomDoc'])
        # resultado =  subir_archivo(resp.content,'rodatest-bucket', nomDoc = r['nomDoc'])
        print("**********PDF SUBIDO**********")
        print("")
else:
    resp_cont = openkm.get_content_doc(response['uuid'])
    print(response['nomDoc'])
    # resultado = subir_archivo(resp_cont.content,'rodatest-bucket', nomDoc = response['nomDoc'])
    print("**********PDF SUBIDO**********")

