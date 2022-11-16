from pickle import TRUE
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet,ViewSet
from django.shortcuts import get_object_or_404
import sys
import requests
import json
import time
from apps.OCR.procesamiento.processViews import OpenKMViewSet

#from apps.OCR.procesamiento.processViews import OpenKMViewSet

#aqui pondremos todo el proceso como tal y usaremos funciones de datetime para pauarlo 
#en la funcion de abajo por lo que esta funcion sera llamada 
#primero el proceso completo se usara de prueba y luego  se le ingresara una variable 
# a la funcion para detenerlo por 'X' dias

#folio = '000079921'
#'DodcID':id_doc,'uuid':data.get("uuid")
#Pcompleto.search_docs()
#Pcompleto.process_docs()

class procesoautomatico(ViewSet):


        def procesocompleto(request):
         
         Pcompleto = OpenKMViewSet() 

         try:   
                     Pcompleto.search_docs(request,folio='000079921')
                     Pcompleto.process_docs(request) 
         except Exception as e:
            print(e)   
         return Response({'message':'archivo automatico no procesado'},status=status.HTTP_200_OK,headers=None)
