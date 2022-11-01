from turtle import clear
import boto3
from trp import Document
import trp.trp2 as t2
from tabulate import tabulate

# S3 Bucket Data
s3BucketName = "rodatest-bucket"
# PlaindocumentName = "media/Clinica_santiago.pdf"
# FormdocumentName = "media/Clinica_santiago.pdf"
TabledocumentName = "media/Clinica Santiago_271715_202103_4486.pdf"
PlaindocumentName = "media/Clinica Santiago_271715_202103_4486.pdf"
FormdocumentName = "media/Clinica Santiago_271715_202103_4486.pdf"
# TabledocumentName = "media/Clinica_santiago.pdf"
PlaindocumentName = "media/Agosto.pdf"
FormdocumentName = "media/Agosto.pdf"

# Amazon Textract client
textractmodule = boto3.client('textract', region_name='us-east-1')

#1. PLAINTEXT detection from documents:
# response = textractmodule.detect_document_text(
#     Document={
#             'S3Object': {
#             'Bucket': s3BucketName,
#             'Name': PlaindocumentName
#         }
#     })

# print('------------- Impresión formato textract ------------------------------')
# for item in response["Blocks"]:
#     if item["BlockType"] == "LINE":
#         print('\033[92m'+item["Text"]+'\033[92m')


# #2. FORM detection from documents:
# response = textractmodule.analyze_document(
#     Document={
#             'S3Object': {
#             'Bucket': s3BucketName,
#             'Name': FormdocumentName
#         }
#     },
#     FeatureTypes=["FORMS"])
# doc = Document(response)
# print ('------------- Impresión formato llave ------------------------------')
# for page in doc.pages:
#     for field in page.form.fields:
#         print("Key: {}, Value: {}".format(field.key, field.value))

#3. Querys:
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
    FeatureTypes=["QUERIES"],
    QueriesConfig={
        "Queries": [{
            "Text": "ss",
            "Alias": "ss"
        },
        {
            "Text": "sss",
            "Alias": "sss"
        }]
    })

print('--------------------------Querys-------------------------')
d = t2.TDocumentSchema().load(response)
page = d.pages[0]
query_answers = d.get_query_answers(page=page)
print(tabulate(query_answers, tablefmt="github"))

# print('-----------------Tables----------------------')
# response = textractmodule.analyze_document(
#     Document={
#             'S3Object': {
#             'Bucket': s3BucketName,
#             'Name': TabledocumentName
#         }
#     },
#     FeatureTypes=["TABLES"])
# doc = Document(response)
# for page in doc.pages:
#      # Print tables
#     for table in page.tables:
#         for r, row in enumerate(table.rows):
#             for c, cell in enumerate(row.cells):
#                 print("Table[{}][{}] = {}".format(r, c, cell.text))


# FeatureTypes=["FORMS"])
doc = Document(response)
print ('------------- Impresión formato llave ------------------------------')
for page in doc.pages:
    for field in page.form.fields:
        print("Key: {}, Value: {}".format(field.key, field.value))
