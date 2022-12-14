from rest_framework import serializers
from apps.management.models import Sistema
import os

def delete_old_file(path_file):
    #Delete old file when upload new one
    if os.path.exists(path_file):
        os.remove(path_file)


class SistemaSerializers(serializers.ModelSerializer):
    name_sis = serializers.ReadOnlyField()
    class Meta:
        model = Sistema
        fields = ('name_sis', 'credencial')

    def update(self, instance, validated_data):
        # delete_old_file(instance.credencial.path)
        return super().update(instance, validated_data)
        
        
