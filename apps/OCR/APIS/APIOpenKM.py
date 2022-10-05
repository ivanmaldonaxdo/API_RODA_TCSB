import requests
from requests.auth import HTTPBasicAuth
import json
from requests.adapters import HTTPAdapter, Retry
import time
import re

#************* CLASE API OPENKM **************
class OpenKm():
    def __init__(self, username, password, url):
        self.auth_creds = HTTPBasicAuth(username, password)
        self.end_point_base = url

    def get_response(self,_url,_params = None):
        _headers = {
            'Accept': 'application/json',
        }
        response = requests.get(_url,headers =_headers, auth = self.auth_creds, params = _params )
        return response

#AGU - ELE - GAS
# url = "{}{}={}" .format(self.end_point_base,'search/find?property=okp:encCobro.folio',_query) //URL BASE
    def get_docs(self, _nombre = None ,_serv = None):
        _prop_base, _operation  = 'okp:encCobro.','search/find'
        # _params =  {'property':'{}{}={}' .format(_prop_base,'tipo_servicio','AGU')}
        # _params =  {'property':'{}{}={}' .format(_prop_base,'folio',_nombre)}
        # _params =  {'folio':_nombre, 'tipo_servicio':_serv} 
        # url = "{}{}" .format(self.end_point_base,_operation)
        # url = "{}{}={}" .format(self.end_point_base,'search/find?property=okp:encCobro.folio',_nombre)
        url = "{}{}={}" .format(self.end_point_base,'search/find?property=okp:encCobro.tipo_servicio',_serv)
        response = self.get_response(url)
        status_code = response.status_code
        if (status_code in range(200,399)):
            print("Codigo de estado es aceptable") 
            print("")
            data = response.json()
            print("")
            # print(data['queryResult'])
            print("")
            # print( "TIPO DATO => {}".format(type(data['queryResult'])))
            tipo_dato = type(data['queryResult'])
            nodo ,uuid= "",""
            is_lista = isinstance(data['queryResult'], list) #evalua si es una lista de varias boletas
            print("ES LISTA? : {} " .format(isinstance(data['queryResult'], list)))
            if is_lista:
                print("**********TEST MUCHAS BOLETAS*********")
                print("")
                # print(data['queryResult'].keys())
                cantidad = 0
                boletas = []
                for d in data['queryResult']:
                    nodo = d["node"]
                    uuid = nodo["uuid"]
                    path_doc = nodo["path"]
                    cantidad+=1
                    # ruta_sep = path_doc.split('/')[-2:-1]
                    nom_doc = path_doc.split('/')
                    nom_doc = nom_doc[-1]
                    # print("BOLETA N° {} - UUID: {}".format(cantidad,uuid))
                    boletas.append(dict(
                        {'path':path_doc, 
                        'uuid':uuid,
                        'nomDoc':nom_doc
                        }
                    ))
                print("TOTAL BOLETAS => {}" .format(cantidad))
                return boletas
            else:
                print("**********TEST UNA BOLETA*********")
                data_node = data['queryResult']['node']
                path,uuid = data_node['path'],data_node['uuid']
                nom_doc = path.split('/')
                nom_doc = nom_doc[-1]

                print("DATA => PATH: {} /n UUID: {}" .format(path,uuid))
                print("")
                boleta = dict(
                        {'path':path, 
                        'uuid':uuid,
                        'nomDoc':nom_doc
                        }
                    )
                return boleta
        else:
            return "ERROR => STATUS_CODE: {} | URL: {}" .format(status_code, response.url)

    #FUNCION PARA DESCARGAR ARCHIVO pdf por UIID 
    def get_content_doc(self,uuid = None):
        url = "http://65.21.188.116:8080/OpenKM/services/rest/document/getContent?docId={}" .format(uuid)
        response = requests.get(url, auth = self.auth_creds)
        status_code = response.status_code
        if (status_code in range(200,399)):
            print("OBTENCION CORRECTA DE CONTENIDO")
            return response
        else:
            return "ERROR EN CODIGO ESTADO => {} ".format(status_code)

    ##PETICION PARA OBTENER METADATA DE ARCHIVOS EJ:      
    def get_doc_by_folio(self,_query = None):
        _metadata = 'folio'
        _prop_base = 'okp:encCobro.'
        _params =  {'property':'{}{}={}' .format(_prop_base,_metadata,_query)}
        url = "{}{}" .format(self.end_point_base,'search/find')
        # url = "{}{}={}" .format(self.end_point_base,'search/find?property=okp:encCobro.folio',_query)
        response = self.get_response(url,_params=_params)
        status_code = response.status_code
        if (status_code in range(200,399)):
            print("Codigo de estado es aceptable") 
            print("")
            data = response.json()  
            # print(len(data['queryResult']))
            print(data)
            cantidad = 0
            for f in data:
                cantidad+=1
            print("")
            print( "Cantidad DATA => {}".format(len(data)))
            print(data['queryResult'].keys())
            data_node = data['queryResult']['node']
            path,uuid = data_node['path'],data_node['uuid']
            print("DATA => PATH: {} /n UUID: {}" .format(path,uuid))
            # return data

            return uuid

        else:
            return "ERROR "    



# print("")
# print("datatype of RESPONSE")

# print(type(response.content))
# now = time.localtime(time.time())
# fecha = time.strftime("%Y_%m_%d", now)
# print(fecha)
# with open("boleta_{}.pdf" .format(fecha), "wb") as pdf:
#     pdf.write(response.content)
# query = {
#     'anio_doc':'2020'
# }

# # http://65.21.188.116:8080/OpenKM/services/rest/search/find?property=okp:encCobro.folio=5293130/&mimeType=application/pdf

# # openkm.get_doc_by_folio(5293130)
#https://www.openkm.com/wiki/index.php/RESTful_Guide#Search


#REFERENCIAS 
#https://docs.openkm.com/kcenter/view/okm-6.4/download-document-with-direct-link.html