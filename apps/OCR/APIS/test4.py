import textractcaller as tc
import trp.trp2 as t2
import boto3

textract = boto3.client('textract', region_name="us-east-1")
q1 = tc.Query(text="ss", alias="ss", pages=["*"])
q2 = tc.Query(text="sss", alias="sss", pages=["*"])
textract_json = tc.call_textract(
    input_document="s3://rodatest-bucket/media/Clinica Santiago_271715_202001_1655.pdf",
    queries_config=tc.QueriesConfig(queries=[q1, q2]),
    features=[tc.Textract_Features.QUERIES],
    force_async_api=True,
    boto3_textract_client=textract)
t_doc: t2.TDocument = t2.TDocumentSchema().load(textract_json)  # type: ignore
for page in t_doc.pages:
    query_answers = t_doc.get_query_answers(page=page)
    for x in query_answers:
        print(f"{x[1]},{x[2]}")