import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
import io
import csv
import time
#from tabulate import tabulate
import json
# from apps.OCR.APIS.textractByQueries import textract
from apps.OCR.APIS.textractByTables import textractTB
# from apps.OCR.APIS.textractByTablesExp import get_table_results
from apps.OCR.APIS.textractByQueriesPages import textract
import re

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

def extraccionOCR(_bucket,query,tables,carpeta = 'media',nomDoc = None):
    json_procesado = dict()
    json_tablas = dict()
    archivo = '{}/{}'.format(carpeta,nomDoc)
    bucket = _bucket
    # print("archivo ",archivo)
    # print("Bucket ", _bucket)

    ############### EXTRACCION POR QUERIES ###############
    # resultado_queries = textract(_bucket, query,archivo)

    ############### EXTRACCION POR QUERIES JSON ###############
    resultado_queries = textract(_bucket = _bucket, _queries_file = query, _documento = archivo)

    print("RESULTADO QUERIES")
    print(resultado_queries)
    print("****************")
    json_procesado.update(resultado_queries)

    ############### RECUPERANDO DATA DE JSON TABLAS ###############
    with open(tables) as tb_json:
        data = tb_json.read().replace("\n", "").replace('ï»¿', "").strip()
    data = json.loads(data)[0]
    json_tablas.update(data)
    list_tablas = json_tablas.get("TABLES")

    try:
        print(list_tablas)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        print(e)

    ############### EXTRACCION POR TABLAS ###############
    resultado_tables = textractTB(_bucket = bucket , _documento = archivo, _list_tablas = list_tablas)

    json_procesado.update(resultado_tables)
    # print(json.dumps(json_procesado, indent=4))

    ###EXTRACCION APARTE
    # textractPages = get_table_results(archivo, list_tablas)
    # print(textractPages)
    return json_procesado

#EMPEZAR ANALISIS DE DOCUMENTO

#references 
#https://www.programiz.com/python-programming/json
#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/