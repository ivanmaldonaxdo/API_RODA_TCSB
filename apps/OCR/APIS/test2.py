import time
import json
from json import dumps, loads
import boto3
from matplotlib.font_manager import json_dump
import trp.trp2 as t2
from tabulate import tabulate
from trp.trp2 import TDocument, TDocumentSchema
from trp.trp2_analyzeid import TAnalyzeIdDocument, TAnalyzeIdDocumentSchema

def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']
        
        return pages


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
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

    job_id = start_job(client, s3_bucket_name, document_name)
    print("ID del proceso: {}".format(job_id))
    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)
        # json_str = json.dumps(response)

    # print(response)

    #Print detected text
    for result_page in response:
        for item in result_page["Blocks"]:
            if item["BlockType"] == "LINE":
                print('\033[94m' + item["Text"] + '\033[0m')
    
# print('--------------------------Querys-------------------------')
# t_doc = TAnalyzeIdDocumentSchema().dump(response)
# d = t2.TDocumentSchema().dump(response)
# query_answers = d.get_query_answers()
# print(query_answers)
# d = t2.TDocumentSchema().load(response)
# t_doc = TDocumentSchema().dump(response)
# t_doc = TAnalyzeIdDocumentSchema().dump(response)
# page = t_doc.pages[0]
# query_answers = t_doc.get_query_answers(page=page)
# print(tabulate(query_answers, tablefmt="github"))
# t_doc = TDocumentSchema().load(response)
# t_doc: t2.TDocument = t2.TDocumentSchema().load(response)  # type: ignore
# t_doc = TAnalyzeIdDocumentSchema().dump(response)
# for page in t_doc.pages:
#     query_answers = t_doc.get_query_answers(page=page)
#     for x in query_answers:
#         print(f"{x[1]},{x[2]}")