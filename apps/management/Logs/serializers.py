from rest_framework import serializers
from apps.management.models import LogSistema

class LogSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(source='fecha_hora',format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model= LogSistema
        fields= ('id', 'id_user', 'cliente', 'payload', 'method', 'response', 'status_code', 'fecha') 