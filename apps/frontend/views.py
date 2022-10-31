from django.shortcuts import render
from django.http import JsonResponse , request
import requests
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def processDocs(request):
    q_folio = request.GET.get('sfolio')
    q_tpServicio = request.GET.get('cbotipo_servicio')
    # render_vacio = render(request, 'frontend/inicio.html')  
    #print("FOLIO =>", q_folio)
    # return render(request, 'frontend/inicio.html')  

    if q_folio == None or q_folio  == "" and q_tpServicio == "Tipo de servicio":
        print("Campo vacio")
        return render(request, 'frontend/inicio.html')  
    else:    
        if q_tpServicio == "Tipo de servicio":
            q_tpServicio = None
        #print("BUSQUEDA => FOLIO: {} - Tipo Servicio: {}".format(q_folio,q_tpServicio) )
        scheme = request.scheme               # http or https
        meta = request.META['HTTP_HOST']
        # print("Dominio => scheme: {} - meta Servicio: {}".format(scheme,meta) )
        
        # domain = Site.objects.get_current().domain
        # print(domain)
        cookies = dict(Cookies=request.COOKIES.get('jwt'))
        print(cookies)
        url = 'http://127.0.0.1:8000/documentos/search_docs/'
        data = {
                "folio":q_folio,
                "tipo_servicio":q_tpServicio,
                "rut_receptor":None
            }
        data = dict(data)
        headers = {'Accept': 'application/json'}
        response = requests.post(url,json = data,headers = headers)
        print("")
        
        # boletas = response.json() if 'detail' not in response.json() else None
        procesados = response.json() 
        print(type(procesados))
        # print(boletas)
        # q_tpServicio = "Tipo de servicio"
        context = {
           'procesados':procesados
        }
        return render(request, 'frontend/inicio.html',context)  


    return render(request, 'frontend/inicio.html')  

def login(request):
    return render(request, 'frontend/login.html')

@login_required
def homeinfo(request):
    return render(request, 'frontend/homeinfo.html')



def test(request):
    return render(request, 'frontend/test.html')

