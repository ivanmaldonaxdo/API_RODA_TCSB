queries_csv = "test.csv"

import csv
from http import client
from typing import Text
import boto3
import trp.trp2 as t2
from tabulate import tabulate
import time
import json

def start_job(s3_bucket_name, document_name): 
    queries = list()
    with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
        reader = csv.reader(queries_csv_file)
        for row in reader:
            queries.append({"Text": row[0].strip(), "Alias": row[1] })
    response = client.start_document_analysis(
        DocumentLocation={
                'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': document_name
                }
        },
        FeatureTypes=["QUERIES"],
        QueriesConfig={
            "Queries": queries
        })
    
    return response["JobId"]

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

if __name__ == "__main__":
    # Document
    s3_bucket_name = "rodatest-bucket"
    document_name = "media/Agosto.pdf"
    region = "us-east-1"
    client = boto3.client('textract', region_name=region)

    job_id = start_job(s3_bucket_name, document_name)
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
            documento.update({alias:respuesta})
        print(documento)

json_object = json.dumps(documento, indent=4)
with open("zzz.json", "w") as outfile:
    outfile.write(json_object)
    