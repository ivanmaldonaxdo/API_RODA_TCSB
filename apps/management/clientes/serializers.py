from rest_framework import serializers
from apps.management.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


    def create(self, validated_data):
        cliente = Cliente(**validated_data)
        cliente.save()
        return cliente

    