from apps.management.models import ConfigCron
from rest_framework import serializers

class SistemaSerializers(serializers.ModelSerializer):
    hora_luz = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    hora_agua = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    hora_gas = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    class Meta:
        model = ConfigCron
        fields = ('hora_luz', 'hora_agua', 'hora_gas',)