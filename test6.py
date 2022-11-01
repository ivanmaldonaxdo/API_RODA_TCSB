import csv
from urllib import response
import boto3
import trp.trp2 as t2
from tabulate import tabulate

s3BucketName = "rodatest-bucket"
FormdocumentName = "media/Clinica Antofagasta_301625_202201_6908.pdf"

textract = boto3.client('textract', region_name='us-east-1')

# def textfunc():
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
                    'Bucket': s3BucketName,
                    'Name': FormdocumentName
                    }
            },
            FeatureTypes=["QUERIES"],
            QueriesConfig={
                "Queries": queries
            })


print(response)
    # d = t2.TDocumentSchema().load(response)
    # page = d.pages[0]
    # query_answers = d.get_query_answers(page=page)
    # print(tabulate(query_answers, tablefmt="github"))