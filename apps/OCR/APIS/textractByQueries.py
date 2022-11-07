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
    print("textfunc")
    print("")
    print("archivo ",_archivo)
    print("Bucket ", _bucket)
    print("Ruta queries ",_query)
    queries_csv = _query
    # queries_csv = '/test.csv'
    queries = list()
    with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
        reader = csv.reader(queries_csv_file)
        for row in reader:
            queries.append({"Text": row[0].strip(), "Alias": row[1] })
        print("QUERIES", queries)
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
            "Queries": queries
        })
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
        print("Resultset page received: {}".format(len(pages)))
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
        print("Resultset page received: {}".format(len(pages)))
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
                print("Query info:")
                print(item["Query"])
            #print(block)
            if item["BlockType"] == "QUERY_RESULT":
                respuesta = item["Text"]
                print("Query answer:")
                print(item["Text"])
            #ALIAS ES EL NOMBRE DE <KEY> Y RESPUESTA ES EL <VALUE>
            documento.update({alias:respuesta})
        print(documento)
    return documento
    # json_object = json.dumps(documento, indent=4)
    # with open("zzz.json", "w") as outfile:
    #     outfile.write(json_object)
# ruta =  'Queries_ENEL_v1_2.csv'    
# resultado_queries = textract("rodatest-bucket", query=ruta,_archivo="media/Clinica Santiago_271715_202203_7352.pdf")
