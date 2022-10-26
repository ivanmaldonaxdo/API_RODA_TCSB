import boto3
import time
import csv
from tabulate import tabulate
import trp.trp2 as t2

queries_csv = 'test.csv'

queries = list()
with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
    reader = csv.reader(queries_csv_file)
    for row in reader:
        queries.append({"Text": row[0].strip(), "Alias": row[1] })

def getJobResults(jobId):
    pages = []
    client = boto3.client('textract', region_name='us-east-1')
    response = client.get_document_analysis(JobId=jobId)
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']
    while(nextToken):
        response = client.get_document_analysis(JobId=jobId, NextToken=nextToken)
        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
    return pages

def get_kv_map(s3BucketName, documentName):
    client = boto3.client('textract', region_name='us-east-1')
    response = client.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': documentName
            }
        },
        FeatureTypes=["QUERIES"],
        QueriesConfig={
            "Queries": queries
        })
    job_id = response['JobId']
    response = client.get_document_analysis(JobId=job_id)
    status = response["JobStatus"]

    
    while(status == "IN_PROGRESS"):
        time.sleep(3)
        response = client.get_document_analysis(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
        
    response = getJobResults(job_id)    
    return response

def query_extraction():

    s3BucketName = "rodatest-bucket"
    documentName = "media/Clinica Santiago_271715_202103_4486.pdf"

    data = get_kv_map(s3BucketName, documentName)
    
    return data

data = query_extraction()

d = t2.TDocumentSchema().load(response)
page = [0]
query_answers = d.get_query_answers(page=page)
print(tabulate(query_answers, tablefmt="github"))