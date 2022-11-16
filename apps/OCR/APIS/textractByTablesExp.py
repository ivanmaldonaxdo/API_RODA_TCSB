import csv
from matplotlib.pyplot import table, text
from trp import Document
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
from pathlib import Path as p
import os

client = boto3.client('textract', region_name='us-east-1')

def get_table_results(archivo,list_tablas,bucket = "rodatest-bucket"):
    # process using pdf
    # get the results
    response = client.analyze_document(Document={
        'S3Object': {
                'Bucket': bucket,
                'Name': archivo
                }
        }, 
        FeatureTypes=['TABLES'])
    doc = Document(response)

    def isFloat(input):
        try:
            float(input)
        except ValueError:
            return False
        return True

    warning = ""

    for page in doc.pages:
        # Print tables
        num_table = 1
        for table in page.tables:
            table_name = 'Table_'+ str(num_table)
            print("********************")
            print("TABLA_" ,num_table)
            num_table+=1
            tabla_horiz = dict()
            if table_name in list_tablas:
                # print(table)
                for r, row in enumerate(table.rows):
                    print(row)
                    print("")
                    cant_values = len(str(row.cells))
                    pattern = "\[\]"
                    print("Largo fila", len(cant_values))
                    # m = re.split(r"\[\]", row)
                    print(type(row.cells))

                    # if cant_values >2:
                    #     print(row.cells)

                    #     m = list(map(lambda x: x, row.cells))
                    #     print(m)

                    # # print(type(r))
                    # itemName  = ""
                    for c, cell in enumerate(row.cells):
                        # print("Table[{}][{}] = {}".format(r, c, cell.text))
                        if(c == 0):
                            itemName = cell.text
                        elif(c == 4 and isFloat(cell.text)):
                            value = float(cell.text)
                            if(value > 1000):
                                warning += "{} is greater than $1000.".format(itemName)
        if(warning):
            print("\nReview needed:\n====================\n" + warning)

#ESTA FUNCION SEPARA LA LINEAS DE TEXTO EN CLAVE VALOR
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
        propiedad = {clave.strip():item_final}
        return propiedad
        # print("Diccionario Final:",propiedad)
    
# with open("json_como_le-dicen.json", "wt",encoding='utf-8') as fout:
#     fout.write(json.dumps(diccionario,indent=4))

def textractTB(archivo,list_tablas):
    table_csv = ""
    print("Lineas")
    print("")
    print(table_csv)
    diccionario = dict()
    for line in table_csv.splitlines():
        # print(line)
        # print()
        # prop = dict()
        
        if line!="":
            # pattern = ' :'
            # replace = ""
            # result = re.sub(pattern, replace, line).strip()
            # print(result)
            propiedad = format_key_value(line)
            if propiedad is not None :
                diccionario.update(propiedad)
                # print(propiedad)
            # diccionario.update(propiedad)
        # print(propiedad)
    print(diccionario)
    return diccionario
# PROCESO get_table_csv_results LLAMA A generate_table_csv() en el cual se obtienen las tablas 

tablas = ['Table_2']


