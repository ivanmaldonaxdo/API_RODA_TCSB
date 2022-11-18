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
client = boto3.client('textract', region_name='us-east-1')
codigo_procesado = None
s3BucketName = "rodatest-bucket"

#EMPEZAR ANALISIS DE DOCUMENTO
def textfunc(_bucket, _query,_archivo):
    # print("textfunc")
    # print("")
    # print("archivo ",_archivo)
    # print("Bucket ", _bucket)
    # print("Ruta queries ",_query)
    queries_csv = _query
    # queries_csv = '/test.csv'
    queries = list()
    with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
        reader = csv.reader(queries_csv_file)
        for row in reader:
            queries.append({"Text": row[0].strip(), "Alias": row[1]})
        # print("QUERIES", queries)
        # Call Textract
        response = client.start_document_analysis(
        DocumentLocation={
                'S3Object': {
                'Bucket': _bucket,
                'Name': _archivo
                }
        },
        FeatureTypes=["QUERIES"],
        QueriesConfig={
            "Queries": [{
                "Text": "NUMBER BELOW FACTURA ELECTRONICA",
                "Alias": "FOLIO/N FACTURA",
                "Pages":["1"]
            },
            {
                "Text": "WHAT IS R.U.T.: IN TOP OF FACTURA ELECTRONICA?",
                "Alias": "RUT_EMISOR",
                "Pages":["1"]
            },
            {
                "Text": "R.U.T.:",
                "Alias": "RUT_CLIENTE",
                "Pages":["1"]
            },
            {
                "Text": "FECHA EMISION",
                "Alias": "FECHA EMISION",
                "Pages":["1"]
            },
            {
                "Text": "DATE TO PAY",
                "Alias": "FECHA DE VENCIMIENTO",
                "Pages":["1"]
            },
            {
                "Text": "SERVICIO CLIENTE",
                "Alias": "Nro CLIENTE",
                "Pages":["1"]
            },
            {
                "Text": "DEMANDA HORAS PUNTA",
                "Alias": "DEMANDA LEIDA HORAS PUNTA",
                "Pages":["1"]
            },
            {
                "Text": "DEMANDA HORAS SUMINISTRADA",
                "Alias": "DEMANDA MAXIMA LEIDA",
                "Pages":["1"]
            },
            {
                "Text": "FACTOR DE POTENCIA",
                "Alias": "FACTOR DE POTENCIA",
                "Pages":["1"]
            },
            {
                "Text": "CONSUMO TOTAL",
                "Alias": "CONSUMO",
                "Pages":["1"]
            }
            ]
        }
        )
        return response['JobId']

#VERIFIFICA SI SE HA REALIZADO ANALISIS
def is_job_complete(job_id):
    time.sleep(1)
    response = client.get_document_analysis(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_analysis(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

def get_job_results(job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_analysis(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_analysis(JobId=job_id, NextToken=next_token)
        pages.append(response)
        # print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']
        
        return pages

def is_job_complete(job_id):
    time.sleep(1)
    response = client.get_document_analysis(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_analysis(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

def get_job_results(job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_analysis(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_analysis(JobId=job_id, NextToken=next_token)
        pages.append(response)
        # print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']

    return pages

#ESTA FUNCION LLAMA AFUNCION TEXTFUNC EN EL CUAL SE DEVUELVE UN JOBID
def textract(_bucket,queryP, _archivo):
    print(queryP)
    # archivo = '{}/{}'.format(carpeta,nomDoc)
    archivo = _archivo
    s3BucketName = _bucket
    job_id = textfunc(_bucket, _query = queryP,_archivo = _archivo)
    documento = dict()

    print("Comenzando el proceso de extracción de información")
    if is_job_complete(job_id):
        print("ID del proceso finalizado: {}".format(job_id))
        codigo_procesado = job_id
        documento.update({"Job_id":job_id})
        response = get_job_results(job_id)
    else:
        print("Error 404")

    # print(response)

    for result_page in response:
        # documento = dict()
        alias = ""
        respuesta = ""
        for item in result_page["Blocks"]:
            if item["BlockType"] == "QUERY":
                alias = item["Query"]["Alias"]
                # print("Query info:")
                # print(item["Query"])
            #print(block)
            if item["BlockType"] == "QUERY_RESULT":
                respuesta = item["Text"]
                # print("Query answer:")
                # print(item["Text"])
            #ALIAS ES EL NOMBRE DE <KEY> Y RESPUESTA ES EL <VALUE>
            documento.update({alias.strip():respuesta})
        # print(documento)
    return documento
