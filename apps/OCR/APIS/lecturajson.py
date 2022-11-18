import json 
import os
from pathlib import Path as p
import sys
import base64
import codecs
# import ....media
# sys.path.append('../../media')
# print()
archivo = 'media/Tables_ENEL_v1_2.json'

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

######## CREA RUTA ABSOLUTA (RUTA COMPLETA)
# archivo = p("Tables_ENEL_v1_2.json")
# print(archivo)
# with open ('../../../media/Tables_ENEL_v1_2.json', "r") as file_json:
#     print(file_json)
#     data = json.load(file_json)

# print(data[0])

    # JSON file
# f = open ('../../../media/Tables_ENEL_v1_2.json', "r")
f = open ('../../../media/Clinica_Santiago_271715_202102_4470.json', "r")

# Reading from file
data = json.loads(f.read())
print(type(data))
objeto = ""
if isinstance(data, list):
    # data = json.load(f)
    print(type(data[0]))
    # print(data[0])
    objeto = data[0]
else:
    objeto = data
    print(objeto)
    print("")
    print("tipo dato objeto ",type(objeto))

str_data = json.dumps(objeto)
# ascii_str_data = str_data.encode('ascii')
# bytes_object = base64.b64encode(ascii_str_data)
bytes_object = base64.b64encode(str_data.encode('utf-8'))

# str_data = str(objeto)
print(str_data)
print("")
print("objeto convertido es: ", type(str_data))
# bytes_object = base64.b64encode(str_data)
print(type(bytes_object))
# with open("queries.pdf", "wb") as pdf:
#     pdf.write(bytes_object.decode('unicode_escape'))
# for i in data:
#     print(i.)
# prin))
# # Reading from file

#referencias
#https://stackoverflow.com/questions/55277431/python-convert-dictionary-to-bytes
#https://www.geeksforgeeks.org/read-json-file-using-python/