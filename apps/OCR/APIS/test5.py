import textractcaller as tc
import trp.trp2 as t2
import boto3

bucket = "rodatest-bucket"
document = "media/Agosto.pdf"
region="us-east-1"

def query_document(bucket, document, region, question):
    # Analyze the document
    client = boto3.client('textract', region_name=region)
    response = client.analyze_document(Document={'S3Object': {'Bucket': bucket, 'Name': document}},
                                       FeatureTypes=["TABLES", "FORMS", "QUERIES"],
                                       QueriesConfig={'Queries':[
                                           {'Text':'{}'.format(question)}
                                       ]})
    
    for block in response['Blocks']:
        if block["BlockType"] == "QUERY":
            print("Query info:")
            print(block["Query"])
        #print(block)
        if block["BlockType"] == "QUERY_RESULT":
            print("Query answer:")
            print(block["Text"])

question = "Client"
query_document(bucket, document, region, question)
