import boto3
import time
from time import sleep
import re
import json
client = boto3.client('textract', region_name='us-east-1')

def startJob(s3BucketName, objectName,_queries_file):
    queries_file = _queries_file
    queries = list()
    ################# LECTURA DEL ARCHIVO JSON DE LAS QUERIES
    f = open (queries_file, "r")
    queries = json.loads(f.read())
    # print(queries)
    global client
    response = None
    response = client.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        },
        FeatureTypes = ["QUERIES", "TABLES"],
        QueriesConfig = queries         
    )
    return response["JobId"]

def isJobComplete(jobId):
    global client
    time.sleep(5)
    response = client.get_document_analysis(JobId=jobId)    
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

pages = []
table_blocks =[]
csv =''
blocks=[]

def getJobResults(jobId,_list_tablas):
    list_tablas = _list_tablas
    global client
    global pages
    global table_blocks
    global blocks
    
    time.sleep(5)
    response = client.get_document_analysis(JobId=jobId)
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None                                            
    if('NextToken' in response):
        nextToken = response['NextToken']
    while(nextToken):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId, NextToken=nextToken)
        pages.append(response)  
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    
    contador=0
    csv = ''
    blocks=[]
    # print(pages)
    data_extracted = dict()
    ################## EXTRACCION DE DATA POR QUERIES ######################
    queries_result = getJobResultsQueries(jobId,pages)
    data_extracted.update(queries_result)
    ################## EXTRACCION DE DATA POR TABLAS ######################
    for item in pages:
        blocks= blocks + pages[contador]['Blocks']                                               
        contador= contador+1
    print(contador)
    
    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
          table_blocks.append(block)
            

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"
    
    if list_tablas is not None:
        for index, table in enumerate(table_blocks):
            csv += generate_table_csv(table, blocks_map, index +1, _list_tablas = list_tablas)
            csv += '\n\n'


        tables_result = csvtext_to_object(csv)
        data_extracted.update(tables_result)
    return data_extracted


########FUNCION QUE DEVUELVE EL RESULTADO DE QUERIES EN DICCIONARIO (JSON)
def getJobResultsQueries(jobId,response):
    json_documento = dict()
    print("Comenzando el proceso de extracción de información")
    # print(response)
    for result_page in response:
        # documento = dict()
        alias = ""
        respuesta = ""
        for item in result_page["Blocks"]:
            if item["BlockType"] == "QUERY":
                alias = item["Query"]["Alias"]
                # print("Query info:")
                # print(item["Query"])
            #print(block)
            if item["BlockType"] == "QUERY_RESULT":
                respuesta = item["Text"]
                # print("Query answer:")
                # print(item["Text"])
            #ALIAS ES EL NOMBRE DE <KEY> Y RESPUESTA ES EL <VALUE>
            if alias != "":
                json_documento.update({alias.strip():respuesta})
        # print(documento)
    # print(json_documento)
    return json_documento

######## ESTA FUNCION GENERA TEXTO A TRAVEZ DE DE CADA FILA DE TABLA
def generate_table_csv(table_result, blocks_map, table_index,_list_tablas):
    list_tablas = _list_tablas
    rows = get_rows_columns_map(table_result, blocks_map)
    csv = ""
    # print("Filas ",rows)
    table_id = 'Table_' + str(table_index)
    if table_id in list_tablas:
        csv = '{0}\n'.format(table_id)
    for row_index, cols in rows.items():
        for col_index, text in cols.items():
            if table_id in list_tablas:
                try:
                    csv += '{}'.format(text)+ " "                
                except:
                    "Error"
            
        if table_id in list_tablas:       
            csv += '\n'

    if table_id in list_tablas:
        csv += '\n\n\n'
    return csv

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    rows[row_index][col_index] = get_text(cell, blocks_map)  #4
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text



#ESTA FUNCION CONVIERTE EL TEXTO CSV DE TABLAS A UN DICCIONARIO (JSON)
def csvtext_to_object(csv):
    response = csv
    diccionario = dict()
    for line in response.splitlines():
        if line!="":
            propiedad = format_key_value(line)
            if propiedad is not None :
                diccionario.update(propiedad)
                # print(propiedad)
            diccionario.update(propiedad)
        # print(propiedad)
    # print(diccionario)
    return diccionario

#ESTA FUNCION FORMATEA LAS LINEAS DEL TEXTO TABLAS
def format_key_value(text):
    if text !="":
        texto = text
        pattern_split = "  +"
        array_texto = re.split(pattern_split, texto.strip())
        # print(array_texto)
        item_final = str(array_texto[-1:][-1])
        # print("Ultimo item ",item_final)
        clave =""
        if len(array_texto)>2:
            index_final = array_texto.index(item_final)
            # print(index_final)
            for i in range (len(array_texto)):
                item = array_texto[i]
                if index_final!= i:
                    if i==0:
                        clave +=" "+item
                    else:
                        clave +="  "+item
                    # print(array_texto[i])
                    # print("No es Ultimo Item")
                    #print("Ultimo item ",array_texto[-1:])
        elif len(array_texto)==1:
            clave = array_texto[0]   
            item_final = " "
        else:
            clave = array_texto[0]      
            
        # print(clave.strip())
        # print(item_final)
        # if clave == "Table:":
        # if clave.strip() !="":
        propiedad = {clave.strip():item_final.strip()}
        return propiedad

# FUNCION GENERAL PARA EXTRAER LA DATA
def textractQTB (s3BucketName, documentName,_queries_file,_tables = None):
    jobId = startJob(s3BucketName, documentName,_queries_file)
    # json_documento = dict()

    print("Started job with id: {}".format(jobId))
    if(isJobComplete(jobId)):
        response = getJobResults(jobId,_tables)
    else:
        print("Error 404")
    
    # print(response)
    return response
    