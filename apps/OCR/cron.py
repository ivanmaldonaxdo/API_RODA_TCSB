from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse, response
from apps.OCR.APIS.APIOpenKM import OpenKm
import sys
import requests
import json
import time


def procesocompleto():   
    #aqui pondremos todo el proceso como tal y usaremos funciones de datetime para pauarlo 
    #en la funcion de abajo por lo que esta funcion sera llamada 
    #primero el proceso completo se usara de prueba y luego  se le ingresara una variable 
    # a la funcion para detenerlo por 'X' dias
    print('aqui va el proceso completo')






#agregar variable de entrada
#path('procesoautomatizado/<int:x>', cron.procesocompleto),
def procesoautomatizado(request,x):
    x = 2
    if x>1 and x<30 :
        print('proceso detenido')

     