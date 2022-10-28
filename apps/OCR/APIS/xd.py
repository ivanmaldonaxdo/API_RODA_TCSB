import csv
import trp.trp2 as t2
import time
from tabulate import tabulate
import boto3

client = boto3.client('textract', region_name='us-east-1')
_bucket = "rodatest-bucket"
archivo = "media/Clinica Antofagasta_301625_202201_6908.pdf"

# def textfunc(_bucket, carpeta = 'media',nomDoc = None):
def start_job(_bucket, archivo):
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


job_id = start_job(_bucket, archivo)
print("Comenzando el proceso de extracción de información")
if is_job_complete(job_id):
    print("ID del proceso finalizado: {}".format(job_id))
    response = get_job_results(job_id)
else:
    print("Error 404")

    # print(response)

for result_page in response:
    for item in result_page["Blocks"]:
        if item["BlockType"] == "QUERY":
            print("Query info:")
            print(item["Query"])
        #print(block)
        if item["BlockType"] == "QUERY_RESULT":
            print("Query answer:")
            print(item["Text"])