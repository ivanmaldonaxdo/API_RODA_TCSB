from dataclasses import field
from itertools import product
from xml.parsers.expat import model
from rest_framework import serializers
from apps.management.models import Sucursal, Contrato_servicio

class SucursalSerializers(serializers.ModelSerializer):

    class Meta:
        model=Sucursal
        fields = '__all__'
    
    def create(self, validated_data):
        sucursal = Sucursal(**validated_data)
        sucursal.save()
        return sucursal

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal 
        fields = ('nom_sucursal', 'cod', 'direccion', 'comuna', 'cliente')
    
    def update(self, instance, validated_data):
        sucursal = super().update(instance, validated_data)
        sucursal.save()
        return sucursal

class ContratoSerializer(serializers.ModelSerializer):
    sucursal_name = serializers.ReadOnlyField(source='sucursal.nom_sucursal')
    proveedor_name = serializers.ReadOnlyField(source='proveedor.nom_proveedor')

    class Meta:
        model= Contrato_servicio
        fields=('num_cliente', 'sucursal_name', 'proveedor_name')

class SucursalModelSerializer(serializers.ModelSerializer):
    contrato_servicio = ContratoSerializer(many=True, source="contrato_servicio_set")
    class Meta:
        model=Sucursal
        fields= '__all__'

class ContratoServiciosSerializer(serializers.ModelSerializer):

    class Meta:
        model= Contrato_servicio
        fields='__all__'
