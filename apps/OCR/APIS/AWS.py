import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
import io
import csv
<<<<<<< HEAD
# import trp.trp2 as t2
>>>>>>>>> Temporary merge branch 2
import time
#from tabulate import tabulate
import json

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

#EMPEZAR ANALISIS DE DOCUMENTO
def textfunc(_bucket, archivo):
    queries_csv = "test.csv"
    queries = list()
    with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
        reader = csv.reader(queries_csv_file)
        for row in reader:
            queries.append({"Text": row[0].strip(), "Alias": row[1] })

        # Call Textract
        response = client.start_document_analysis(
        DocumentLocation={
                'S3Object': {
                'Bucket': _bucket,
                'Name': archivo
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

def textract(_bucket, carpeta = 'media',nomDoc = None):
    archivo = '{}/{}'.format(carpeta,nomDoc)
    job_id = textfunc(_bucket, archivo)
    print("Comenzando el proceso de extracción de información")
    if is_job_complete(job_id):
        print("ID del proceso finalizado: {}".format(job_id))
        response = get_job_results(job_id)
    else:
        print("Error 404")

    # print(response)

    for result_page in response:
        documento = dict()
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
    json_object = json.dumps(documento, indent=4)
    with open("zzz.json", "w") as outfile:
        outfile.write(json_object)


