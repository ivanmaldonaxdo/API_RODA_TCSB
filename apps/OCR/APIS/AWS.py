import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
import io

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