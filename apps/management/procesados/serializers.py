from rest_framework import serializers
from apps.management.models import Documento
from rest_framework import serializers

class DocumentoSerializer(serializers.ModelSerializer):
    rut_sucursal = serializers.ReadOnlyField(source='sucursal.rut_sucursal')
    fecha = serializers.DateTimeField(source='fecha_procesado',format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model= Documento
        fields=('nom_doc', 'folio', 'fecha', 'rut_sucursal', 'procesado', 'documento')
