from apps.management.models import ConfigCron
from rest_framework import serializers

class SistemaSerializers(serializers.ModelSerializer):
    hora_exec = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    fecha = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = ConfigCron
        fields = ('hora_exec','fecha')


class CronSerializer(serializers.ModelSerializer):
    hora_exec = serializers.TimeField(format='%H:%M')
    fecha = serializers.DateField(format='%Y-%m-%d')
    status = serializers.ReadOnlyField()
    class Meta:
        model = ConfigCron
        fields = '__all__'


