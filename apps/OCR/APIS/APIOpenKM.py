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

    def get_response(self,_url,_params = None, _headers = {'Accept': 'application/json'}):
        headers = _headers
        response = requests.get(_url,headers = headers, auth = self.auth_creds, params = _params )
        return response
        
    #region GET_DOCS
    #AGU - ELE - GAS
    def get_docs(self, _folio = None ,_serv = None , _path = None, _anio= None):
        # params = {'path':_path}
        url = "{}{}" .format(self.end_point_base,'search/find')
        list_params = [('folio',_folio),('tipo_servicio',_serv),('anio_doc',_anio)]
        properties = self.get_list_params(list_params)
        print("Propiedades => {}" .format(properties))
        params = {'property':properties}
        response = self.get_response(url,params)
        status_code = response.status_code
        if (status_code in range(200,399)):
            print("Codigo de estado {}" .format(status_code)) 
            data = response.json()
            try:
                tipo_dato = type(data['queryResult'])
                nodo ,uuid= "",""
                is_lista = isinstance(data['queryResult'], list) #evalua si es una lista de varias boletas
                print("ES LISTA? : {} " .format(isinstance(data['queryResult'], list)))
                if is_lista:
                    print("**********TEST MUCHAS BOLETAS*********")
                    print("")
                    cantidad = 0
                    boletas = []
                    for d in data['queryResult']:
                        nodo = d["node"]
                        uuid = nodo["uuid"]
                        path = nodo["path"]
                        cantidad+=1
                        nom_doc = path.split('/')
                        nom_doc = nom_doc[-1]
                        # print("BOLETA N° {} - UUID: {}".format(cantidad,uuid))
                        boletas.append(dict(
                            {'path':path, 
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
                            })
                    return boleta
            except:
                print("NO EXISTEN OCURREENCIAS")
                return {}
        else:
            print("ERROR => STATUS_CODE: {} | URL: {}" .format(status_code, response.url))
            return {}
    #endregion GET_DOCS

    #FUNCION PARA DESCARGAR ARCHIVO pdf por UIID 
    def get_content_doc(self,uuid = None):
        url = "{}{}" .format(self.end_point_base,'document/getContent')
        params = {'docId':uuid}
        response = self.get_response(url,_params = params, _headers = None)
        status_code = response.status_code
        if (status_code in range(200,399)):
            print("OBTENCION CORRECTA DE CONTENIDO")
            return response
        else:
            return "ERROR EN CODIGO ESTADO => {} ".format(status_code)

    def get_list_params(self,_list_params,_prop_base = None):
        queries = []
        for l in _list_params:
            # print("PARAM > {}" .format(l))
            if l[1] is not None:
                # print("PARAM > {}" .format('okp:encCobro.{}={}'.format(l[0],l[1])))
                query = 'okp:encCobro.{}={}'.format(l[0],l[1])
                queries.append(query)
        return queries
    ##PETICION PARA OBTENER METADATA DE ARCHIVOS EJ:      
    def get_doc_by_folio(self,_query = None):
        _metadata = 'folio'
        _prop_base = 'okp:encCobro.'
        _params =  {'property':'{}{}={}' .format(_prop_base,_metadata,_query)}
        url = "{}{}" .format(self.end_point_base,'search/find')
        response = self.get_response(url,_params=_params)
        status_code = response.status_code
        if (status_code in range(200,399)):
            print("Codigo de estado es aceptable") 
            print("")
            data = response.json()  

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
            return uuid

        else:
            return "ERROR"
# url = "{}{}={}{}" .format(self.end_point_base,'propertyGroup/hasGroup?nodeId',path,'&grpName=okg:encCobro')

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

#REFERENCIAS 
#https://docs.openkm.com/kcenter/view/okm-6.4/download-document-with-direct-link.html
#https://www.openkm.com/wiki/index.php/RESTful_Guide#Search
#http://65.21.188.116:8080/OpenKM/services/rest/api-docs?url=/OpenKM/services/rest/swagger.json#/search-service/find
