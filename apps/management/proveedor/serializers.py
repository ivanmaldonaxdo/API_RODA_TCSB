from rest_framework import serializers
from apps.management.models import Proveedor
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots

class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = ('nom_proveedor', 'rut_proveedor', 'contacto', 'servicio')

    def create(self, validated_data):
        proveedor = Proveedor(**validated_data)
        proveedor.save()
        return proveedor
    
class UpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Proveedor
        fields = ('nom_proveedor', 'rut_proveedor', 'contacto', 'servicio')

    def update(self, instance, validated_data):
        proveedor = super().update(instance, validated_data)
        proveedor.save()
        return proveedor

    
