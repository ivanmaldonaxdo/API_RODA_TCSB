from rest_framework import serializers
from apps.management.models import Documento
from rest_framework import serializers

class DocumentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documento
        fields = '__all__'

