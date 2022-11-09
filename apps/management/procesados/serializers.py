from rest_framework import serializers
from apps.management.models import Documento
from rest_framework import serializers

class DocumentoSerializer(serializers.ModelSerializer):
    rut_sucursal = serializers.ReadOnlyField(source='sucursal.rut_sucursal')

    class Meta:
        model= Documento
        fields=('nom_doc', 'folio', 'fecha_procesado', 'rut_sucursal', 'procesado', 'documento')


