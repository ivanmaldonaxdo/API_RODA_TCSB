from rest_framework import serializers
from apps.management.models import Documento,Sucursal,Contrato_servicio
from rest_framework import serializers
from apps.management.sucursales.serializers import SucursalSerializers,ContratoSerializer,SucursalModelSerializer
# from C:\Users\IVAN-PC\Documents\PORTAFOLIO\IT2\Transcriptor\apps\management\procesados\serializers.py

class DocumentosSerializers(serializers.ModelSerializer):
    # rut_sucursal = serializers.ReadOnlyField(source='sucursal.rut_sucursal')
    # id_sucursal = serializers.ReadOnlyField(source='sucursal.id')
    # sucursal = SucursalSerializers(many = False)
    # contrato_servicio
    num_cliente = serializers.ReadOnlyField(source='contrato_servicio.num_cliente')
    fecha = serializers.DateTimeField(source='fecha_procesado',format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model= Documento
        # fields='__all__'

        fields=('nom_doc', 'folio', 'fecha', 'procesado', 'documento','num_cliente')


class ContratoSerializer(serializers.ModelSerializer):
    num_cliente = serializers.ReadOnlyField(source='contrato_servicio.num_cliente')
    sucursal = serializers.ReadOnlyField(source='sucursal.id')
    # documento = DocumentosSerializers(source='documento_set',many = True)
    # proveedor_name = serializers.ReadOnlyField(source='proveedor.nom_proveedor')

    class Meta:
        model= Contrato_servicio
        fields='__all__'


# class DocumentoModelSerializer(serializers.ModelSerializer):
#     contrato_servicio = ContratoSerializer(many=True, source="contrato_servicio_set")
#     class Meta:
#         model = Documento
#         fields= '__all__' 
