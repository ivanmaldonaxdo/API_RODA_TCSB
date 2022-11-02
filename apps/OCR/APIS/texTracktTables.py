import csv
from matplotlib.pyplot import table, text
# import trp.trp2 as t2
import time
from tabulate import tabulate
import boto3
import sys
from collections import defaultdict
import re
from pprint import pprint
import json
import time
import pandas as pd
from pathlib import Path as p
import os

client = boto3.client('textract', region_name='us-east-1')
_bucket = "rodatest-bucket"

archivo = "media/Clinica Santiago_271715_202103_4486.pdf"

def get_table_csv_results(archivo,list_tablas,bucket = "rodatest-bucket"):
    # process using pdf
    # get the results
    response = client.analyze_document(Document={
        'S3Object': {
                'Bucket': _bucket,
                'Name': archivo
                }
        }, 
        FeatureTypes=['TABLES'])
    
    blocks=response['Blocks']
    # pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1,list_tablas=list_tablas)
        csv += '\n\n' 
        # print(csv)       
        print("*"*25)
    return csv

    # print(lista_textos)
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
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
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

def generate_table_csv(table_result, blocks_map, table_index,list_tablas):
    rows = get_rows_columns_map(table_result, blocks_map)
    csv = ""
    # print("Filas ",rows)
    table_id = 'Table_' + str(table_index)
    if table_id in list_tablas:
        csv = 'Table: {0}\n\n'.format(table_id)
    tabla_object = dict()
    for row_index, cols in rows.items():
        # print("Columnas" ,cols)
        for col_index, text in cols.items():
            # print("text" ,text)
            if table_id in list_tablas:
            #     # print("No Se  {}" .format(table_id))
            #         # print(csv)
                try:
                    texto ='{}'.format(text)+ " "
                    # print(texto.strip())
                    # tabla_object.update(format_key_value(texto.strip()))
                    csv += '{}'.format(text)+ " "
                    # print( csv[col_index][row_index])
                
                except:
                    "Error"
            

        if table_id in list_tablas:       
            csv += '\n'
        # print(csv[0])
        # if "Table: " in csv:
        #     print("XD")
    if table_id in list_tablas:
        csv += '\n\n\n'
    # print(csv)
    return csv
    
def generate_table_json(table_result, blocks_map, table_index,list_tablas):
    # rows = get_rows_columns_map(table_result, blocks_map)
    print("Filas ",rows)
    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ""
        csv += '\n'
        
    csv += '\n\n\n'
    return csv

def format_key_value(text):
    if text =="":
        texto = text
        texto = texto.replace(" ","_")
        # print(texto)
        texto = texto.strip()
        array_texto = texto.split("__")
        # print(array_texto)
        item_final = str(array_texto[-1:][-1])

        # print("Ultimo item ",item_final)
        clave =""
        query = dict()
        if len(array_texto)>2:
            index = array_texto.index(item_final)
            # print(index)
            for i in range (len(array_texto)):
                item = array_texto[i]
                # print(array_texto[i])
                if index!= i:
                    if i==0:
                        clave +="  "+item
                    else:
                        clave +=" - "+item

                    # print("Ultimo Item")
                    #print("Ultimo item ",array_texto[-1:])
        else:
            clave = array_texto[0]
            valor = item_final
        clave = clave.strip().replace(" -", " ").strip()
        valor = item_final
        query.update({clave:item_final})         
        print("KEY ",clave.strip())
        print("VALUE ",valor)
        return query

    
# print(format_key_value("CARGO POR DEMANDA EN H.P.  6.457,8  1.868  12.063.170"))
# # "CERTIFICADO ENERGIA LIMPIA    690.112"
# print(format_key_value("CERTIFICADO ENERGIA LIMPIA    690.112"))

# # print("")
# print(format_key_value("CARGO POR DEMANDA EN H.P.  12.063.170"))

# some_table = "table_1"
# if some_table in tablas:
#     print("Se encuentra {}" .format(some_table)) 

tablas = ["Table_1","Table_2"]
print("Tablas especificas a extraer data",tablas)

table_csv = get_table_csv_results(archivo,list_tablas=tablas)
print(table_csv)
with open("DOC.csv", "wt") as fout:
    fout.write(table_csv)

# path = p('DOC.csv').re
# print(path)

# def create_full_path(rel_path):
#     absolute_path = os.path.dirname(__file__)
#     relative_path = rel_path
#     full_path = os.path.join(absolute_path, relative_path)
#     return full_path

# csv_path = create_full_path("DOC.csv")
# json_path = create_full_path("doc.json")

# print()

# with open("./DOC.csv", 'rb') as file:
#   csvreader = csv.reader(file)
#   for row in csvreader:
#     try:
#         print(row[0])
#     except:
#         XD = none

# with open("./DOC.csv", 'rb') as file:
#   csvreader = csv.reader(file)
#   for row in csvreader:
#     try:
#         print(row[0])
#     except:
#         XD = none
# df = pd.read_csv(csv_path,on_bad_lines='skip')
# print(df)
# df2 = df.to_json(json_path)
# print(df2)
# PROCESO get_table_csv_results LLAMA A generate_table_csv()