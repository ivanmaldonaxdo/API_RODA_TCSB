from msilib.schema import Feature
from trp import Document
import boto3

s3BucketName = "rodatest-bucket"
object_name = "media/Clinica Antofagasta_301625_202201_6908.pdf"

textractmodule = boto3.client('textract', region_name='us-east-1')

response = textractmodule.analyze_document(
    Document={
            'S3Object': {
            'Bucket': s3BucketName,
            'Name': object_name
        }
    },
    FeatureTypes=["TABLES", "FORMS"])
    #FeatureTypes=["FORMS"])
doc = Document(response)

# Iterate over elements in the document
for page in doc.pages:
    # Print lines and words
    # for line in page.lines:
    #     print("Line: {}--{}".format(line.text, line.confidence))
    #     for word in line.words:
    #         print("Word: {}--{}".format(word.text, word.confidence))

    # Print tables
    for table in page.tables:
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}-{}".format(r, c, cell.text, cell.confidence))

    # # Print fields
    # for field in page.form.fields:
    #     print("Field: Key: {}, Value: {}".format(field.key, field.value))

    # # Get field by key
    # print("Get field by key")
    # key = "TOTAL $"
    # field = page.form.getFieldByKey(key)
    # if(field):
    #     print("Field: Key: {}, Value: {}".format(field.key, field.value))

    # # Search fields by key
    # print("Search fields by key")
    # key = "R.U.T"
    # fields = page.form.searchFieldsByKey(key)
    # for field in fields:
    #     print("Field: Key: {}, Value: {}".format(field.key, field.value))