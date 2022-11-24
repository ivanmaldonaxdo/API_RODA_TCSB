from apps.management.models import ConfigCron
from rest_framework import serializers

class SistemaSerializers(serializers.ModelSerializer):
    hora_exec = serializers.TimeField(format='%H:%M', input_formats='%H:%M')
    class Meta:
        model = ConfigCron
        fields = ('hora_exec',)


class Servicios(object):
	def __init__(self, choices, multiplechoices):
		self.choices = choices
		self.multiplechoices = multiplechoices

# create a tuple
SERVICIOS_CHOICES =(
	(1, "ELE"),
	(2, "AGU"),
	(3, "GAS"),
)

# # create a serializer
# class GeeksSerializer(serializers.Serializer):
# 	# initialize fields
# 	choices = serializers.ChoiceField(
# 						choices = SERVICIOS_CHOICES)
# 	multiplechoices = serializers.MultipleChoiceField(
# 						choices = SERVICIOS_CHOICES)


class CronSerializer(serializers.ModelSerializer):
    hora_exec = serializers.TimeField(format='%H:%M')
    cursor = serializers.ChoiceField(
 						choices = SERVICIOS_CHOICES)
    status = serializers.ReadOnlyField()
    class Meta:
        model = ConfigCron
        fields = '__all__'


