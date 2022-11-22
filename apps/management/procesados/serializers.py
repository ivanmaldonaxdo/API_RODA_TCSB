from rest_framework import serializers
from apps.management.models import Documento,Sucursal,Contrato_servicio
from rest_framework import serializers
from apps.management.sucursales.serializers import SucursalSerializers,ContratoSerializer,SucursalModelSerializer
# from C:\Users\IVAN-PC\Documents\PORTAFOLIO\IT2\Transcriptor\apps\management\procesados\serializers.py

class DocumentoSerializer(serializers.ModelSerializer):
    rut_sucursal = serializers.ReadOnlyField(source='sucursal.rut_sucursal')
    id_sucursal = serializers.ReadOnlyField(source='sucursal.id')
    sucursal = SucursalSerializers(many = False)
    num_cliente = ContratoSerializer(many = True,source='contrato_servicio_set')
    fecha = serializers.DateTimeField(source='fecha_procesado',format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model= Documento
        fields=('nom_doc', 'folio', 'fecha', 'rut_sucursal', 'procesado', 'documento','id_sucursal','sucursal','num_cliente')
