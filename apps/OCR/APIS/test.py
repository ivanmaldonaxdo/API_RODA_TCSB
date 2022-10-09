from turtle import clear
import boto3
from trp import Document

# S3 Bucket Data
s3BucketName = "rodatest-bucket"
# PlaindocumentName = "media/Clinica_santiago.pdf"
# FormdocumentName = "media/Clinica_santiago.pdf"
# TabledocumentName = "media/Clinica_santiago.pdf"
PlaindocumentName = "media/Agosto.pdf"
FormdocumentName = "media/Agosto.pdf"

# Amazon Textract client
textractmodule = boto3.client('textract', region_name='us-east-1')

#1. PLAINTEXT detection from documents:
response = textractmodule.detect_document_text(
    Document={
            'S3Object': {
            'Bucket': s3BucketName,
            'Name': PlaindocumentName
        }
    })
print('------------- Impresión formato textract ------------------------------')
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print('\033[92m'+item["Text"]+'\033[92m')


#2. FORM detection from documents:
response = textractmodule.analyze_document(
    Document={
            'S3Object': {
            'Bucket': s3BucketName,
            'Name': FormdocumentName
        }
    },
    FeatureTypes=["FORMS"])
doc = Document(response)
print ('------------- Impresión formato llave ------------------------------')
for page in doc.pages:
    for field in page.form.fields:
        print("Key: {}, Value: {}".format(field.key, field.value))