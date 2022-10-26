queries_csv = "test.csv"

import csv
from http import client
import boto3
import trp.trp2 as t2
from tabulate import tabulate
import time
import json

queries = list()
with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
    reader = csv.reader(queries_csv_file)
    for row in reader:
        queries.append({"Text": row[0].strip(), "Alias": row[1] })

def start_job(s3_bucket_name, document_name):
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
    document_name = "media/Clinica Santiago_271715_202103_4486.pdf"
    region = "us-east-1"
    client = boto3.client('textract', region_name=region)

    job_id = start_job(s3_bucket_name, document_name)
    print("ID del proceso: {}".format(job_id))
    if is_job_complete(job_id):
        response = get_job_results(job_id)
        # json_str = json.dumps(response)

    # print(response)

    #Print detected text
    for result_page in response:
        d = t2.TDocumentSchema().load(response)
        print(d)
        # page = d.pages[0]
        # query_answers = d.get_query_answers(page=page)
        # print(tabulate(query_answers, tablefmt="github"))