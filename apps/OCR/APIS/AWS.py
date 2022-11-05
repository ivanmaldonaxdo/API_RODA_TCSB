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

def extraccionOCR(_bucket,query,carpeta = 'media',nomDoc = None):
    json_procesado = dict()
    archivo = '{}/{}'.format(carpeta,nomDoc)
    print("archivo ",archivo)
    print("Bucket ", _bucket)
    # print("Ruta queries ",ruta_queries)
    resultado_queries = textract(_bucket, query,archivo)
    # resultado_tablas = 'media/Tables_ENEL_v1_2.json'
    # id_proceso = codigo_procesado
    # json_procesado.update(resultado_queries)
    # return json_procesado


#EMPEZAR ANALISIS DE DOCUMENTO