from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse, response
from apps.OCR.APIS.APIOpenKM import OpenKm
import sys
import requests
import json
import time
from apps.OCR.procesamiento.processViews import OpenKMViewSet



def procesocompleto(requests):   
    #aqui pondremos todo el proceso como tal y usaremos funciones de datetime para pauarlo 
    #en la funcion de abajo por lo que esta funcion sera llamada 
    #primero el proceso completo se usara de prueba y luego  se le ingresara una variable 
    # a la funcion para detenerlo por 'X' dias
    Pcompleto = OpenKMViewSet()
    Pcompleto.search_docs()
    Pcompleto.process_docs()
    Pcompleto.probar_creds()
    Pcompleto.openkm_creds()
    Pcompleto.credenciales()
    print('funciona')
    return HttpResponse("proceso funcionando")






#agregar variable de entrada
#path('procesoautomatizado/<int:x>', cron.procesocompleto),
def procesoautomatizado(request,x):
    x = 2
    if x>1 and x<30 :
        print('proceso detenido')

    return HttpResponse (request)
     