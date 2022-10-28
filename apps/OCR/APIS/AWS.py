import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
import io
import csv
import trp.trp2 as t2
from tabulate import tabulate

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

def textfunc(_bucket, carpeta = 'media',nomDoc = None):
    archivo = '{}/{}'.format(carpeta,nomDoc)
    textract = boto3.client('textract', region_name='us-east-1')
    queries_csv = "test.csv"
    queries = list()
    with open(queries_csv, mode='r', encoding='utf-8-sig') as queries_csv_file:
        reader = csv.reader(queries_csv_file)
        for row in reader:
            queries.append({"Text": row[0].strip(), "Alias": row[1] })

        # Call Textract
        response = textract.analyze_document(
            Document={
                    'S3Object': {
                    'Bucket': _bucket,
                    'Name': archivo
                    }
            },
            FeatureTypes=["QUERIES"],
            QueriesConfig={
                "Queries": queries
            })

    d = t2.TDocumentSchema().load(response)
    page = d.pages[0]
    query_answers = d.get_query_answers(page=page)
    print(tabulate(query_answers, tablefmt="github"))