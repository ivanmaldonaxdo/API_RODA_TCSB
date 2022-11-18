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
# codigo_procesado = None
# s3BucketName = "rodatest-bucket"

#EMPEZAR ANALISIS DE DOCUMENTO
def textfunc(_bucket, _queries_file,_documento):
    queries_file = _queries_file
    # queries_csv = '/test.csv'
    queries = list()
    ################# LECTURA DEL ARCHIVO JSON DE LAS QUERIES
    f = open (queries_file, "r")
    queries = json.loads(f.read())
    # print("QUERIES LOADED")
    # print("")
    # print(queries)

    response = client.start_document_analysis(
        DocumentLocation={
                'S3Object': {
                'Bucket': _bucket,
                'Name': _documento
                }
        },
        FeatureTypes=["QUERIES"],
        QueriesConfig = queries
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
def textract(_bucket,_queries_file, _documento):
    queries_file = _queries_file
    print(queries_file)
    # archivo = '{}/{}'.format(carpeta,nomDoc)
    documento = _documento
    s3BucketName = _bucket
    job_id = textfunc(s3BucketName, _queries_file = queries_file, _documento = documento)
    json_documento = dict()
    print("Comenzando el proceso de extracción de información")
    if is_job_complete(job_id):
        print("ID del proceso finalizado: {}".format(job_id))
        codigo_procesado = job_id
        json_documento.update({"Job_id":job_id})
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
            json_documento.update({alias.strip():respuesta})
        # print(documento)
    return json_documento
