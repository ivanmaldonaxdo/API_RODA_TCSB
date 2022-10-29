from django.shortcuts import render
from django.http import JsonResponse , request
import requests
import json

# Create your views here.

def inicio(request):
    q_folio = request.GET.get('folio')
    q_tpServicio = request.GET.get('tipo_servicio')
    if q_tpServicio =="Tipo de servicio":
        q_tpServicio = None
    print("BUSQUEDA => FOLIO: {} - Tipo Servicio: {}".format(q_folio,q_tpServicio) )
    scheme = request.scheme               # http or https
    meta = request.META['HTTP_HOST']
    # print("Dominio => scheme: {} - meta Servicio: {}".format(scheme,meta) )
    
    # domain = Site.objects.get_current().domain
    # print(domain)
    url = 'http://127.0.0.1:8000/documentos/search_docs/'
    data = {
            "folio":q_folio,
            "tipo_servicio":q_tpServicio,
            "rut_receptor":"" 
        }
    headers = {'Accept': 'application/json'}
    response = requests.post(url,json = data,headers = headers)  
    print("")
    # print(response.json())
    return render(request, 'frontend/inicio.html', {'boletas': response.json()})  

def login(request):
    return render(request, 'frontend/login.html')

def homeinfo(request):
    return render(request, 'frontend/homeinfo.html')

