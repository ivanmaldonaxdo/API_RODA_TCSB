from rest_framework import serializers
from apps.management.models import Cliente
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots, format_rut_with_dots

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        exclude = ('sistema',)


    def create(self, validated_data):
        cliente = Cliente(**validated_data)
        cliente.save()
        return cliente



class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente 
        fields = ('nom_cli', 'rut_cliente', 'razon_social')
    
    

    