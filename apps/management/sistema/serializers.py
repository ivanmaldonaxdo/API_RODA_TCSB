from rest_framework import serializers
from apps.management.models import Sistema


class SistemaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Sistema
        fields = ('name_sis', 'credencial')

    def update(self, instance, validated_data):
        proveedor = super().update(instance, validated_data)
        proveedor.save()
        return proveedor
