from apps.management.models import ConfigCron
from rest_framework import serializers

class SistemaSerializers(serializers.ModelSerializer):
    hora_luz = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    hora_agua = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    hora_gas = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    class Meta:
        model = ConfigCron
        fields = ('hora_luz', 'hora_agua', 'hora_gas',)


class CronSerializer(serializers.ModelSerializer):
    hora_luz = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    hora_agua = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    hora_gas = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    # cron = ConfigCron.objects.get(id=1)
    # servicios = ['AGU','ELE','GAS']
    # if cron.status != 'Desactivado' or cron.status !='Terminado o En espera':
    #     ejecutandose = serializers.CharField(servicios[cron.cursor])
    
    # proxima_tarea = serializers.CharField(servicios[cron.cursor + 1])

    class Meta:
        model = ConfigCron
        fields = '__all__'


