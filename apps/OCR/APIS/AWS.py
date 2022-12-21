import boto3
import io
import json
from apps.OCR.APIS.textractByQueriesTables import textractQTB
import re
import sys
# from apps.OCR.APIS.textractByQueries import textract, codigo_procesado
client = boto3.client('textract', region_name='us-east-1')

def subir_archivo(archivo,_bucket,carpeta = 'media',nomDoc = None):
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(_bucket)
    # fo = io.BytesIO(r.content)
    # 'fac-agua/
    result = bucket.upload_fileobj(io.BytesIO(archivo), '{}/{}'.format(carpeta,nomDoc))
    return result

def listar_buckets():
    session = boto3.Session()
    s3 = session.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)

def extraccionOCR(_bucket,query,tables = None,carpeta = 'media',nomDoc = None):
    json_procesado = dict()
    json_tablas = dict()
    archivo = '{}/{}'.format(carpeta,nomDoc)
    bucket = _bucket
    queries = query
    # print("archivo ",archivo)
    # print("Bucket ", _bucket)
    ############### RECUPERANDO DATA DE JSON TABLAS ###############
    with open(tables) as tb_json:
        data = tb_json.read().replace("\n", "").replace('ï»¿', "").strip()
    data = json.loads(data)[0]
    json_tablas.update(data)
    list_tablas = json_tablas.get("TABLES")
    ################ VERIFICA EL LARGO DE ELEMENTOS EN LA LISTA DE LA TABLA 
    # print(type(list_tablas))
    print("Largo Tablas", len(list_tablas))
    list_tablas = (list_tablas if len(list_tablas) > 0 else None)
    try:
        # print(list_tablas)
        json_procesado = textractQTB(bucket, archivo, queries,list_tablas)
        print(json.dumps(json_procesado, indent = 4))
        return json_procesado
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        print("")
        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        print(e)
        # tablas_json = dict()
        # with open(tables) as json_file:
        #     data = json.load(json_file)
        # # print(data[0])
        # tablas_json.update(data[0])
        #     # json_creds.update(data)
        return None

    ###EXTRACCION APARTE
    # textractPages = get_table_results(archivo, list_tablas)
    # print(textractPages)

#EMPEZAR ANALISIS DE DOCUMENTO

#references 
#https://www.programiz.com/python-programming/json
#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/