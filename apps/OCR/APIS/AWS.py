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
from apps.OCR.APIS.textractByQueries import textract
from apps.OCR.APIS.textractByTables import textractTB
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
    # print("archivo ",archivo)
    # print("Bucket ", _bucket)

    ############### EXTRACCION POR QUERIES ###############
    resultado_queries = textract(_bucket, query,archivo)
    json_procesado.update(resultado_queries)
    ############### RECUPERANDO DATA DE JSON TABLAS ###############
    with open(tables) as tb_json:
        data = tb_json.read().replace("\n", "").replace('ï»¿', "").strip()
    data = json.loads(data)[0]
    json_tablas.update(data)
    list_tablas = json_tablas.get("TABLES")
    ############### EXTRACCION POR TABLAS ###############
    resultado_tables = textractTB(archivo, list_tablas)

    json_procesado.update(resultado_tables)
    # print(json.dumps(json_procesado, indent=4))
    return json_procesado

#EMPEZAR ANALISIS DE DOCUMENTO

#references 
#https://www.programiz.com/python-programming/json
#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/