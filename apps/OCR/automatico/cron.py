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
from rest_framework.decorators import action

#from apps.OCR.procesamiento.processViews import OpenKMViewSet

#aqui pondremos todo el proceso como tal y usaremos funciones de datetime para pauarlo 
#en la funcion de abajo por lo que esta funcion sera llamada 
#primero el proceso completo se usara de prueba y luego  se le ingresara una variable 
# a la funcion para detenerlo por 'X' dias

#folio = '000079921'
#'DodcID':id_doc,'uuid':data.get("uuid")
#Pcompleto.search_docs()
#Pcompleto.process_docs()


#metadata = self.openkm.get_metadata(data.get("uuid"))

class procesoautomatico(ViewSet):

        @action(detail=False,methods = ['POST'],url_name="proceso_automatico")
        def procesocompleto(request):
         
         Pcompleto = OpenKMViewSet() 

         try:   
                  data = Pcompleto.search_docs(request,folio='000079921')
                  Pcompleto.process_docs(request,data) 

         except Exception as e:
            print(e)   
         return Response({'message':'archivo automatico no procesado'},status=status.HTTP_200_OK,headers=None)
