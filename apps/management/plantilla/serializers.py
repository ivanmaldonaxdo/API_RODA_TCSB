from rest_framework import serializers
from apps.management.models import Plantilla
from rest_framework.serializers import Serializer, FileField

class PlantillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plantilla
        fields = '__all__'

class UpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plantilla
        fields = '__all__'