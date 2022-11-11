
# from django.db import connections
# from apps.management.models import Plantilla,Cliente,Sucursal,Documento
# from django.db.models import Q
import json
import os
import csv
from django.conf import settings# from django.core.files.storage
from Transcriptor import settings
bd = settings.DATABASES

for k,v in bd.items():
    print(key," : ",value)
