from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from apps.management.cron.serializers import CronSerializer
import subprocess
from apps.management.models import ConfigCron
from django.shortcuts import get_object_or_404
from django.http import Http404

class StatusForCron(viewsets.GenericViewSet):
    serializer_class = CronSerializer
    model = ConfigCron

    def get_queryset(self):
        queryset=ConfigCron.objects.all().first()
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk = None): #Detalle de un usuario
        cron = self.get_object(pk)
        cron_serializer = self.serializer_class(cron)
        return Response(cron_serializer.data, status= status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        cron  = self.get_object(pk)
        if cron.is_active == True:
            cron.is_active=False
            cron.status='Desactivado'
            cron.save()
            subprocess.run(["sudo", "service", "cron", "stop"])
            return Response ({
                'message': 'CRON is INACTIVE'
            }, status=status.HTTP_200_OK)
        elif cron.is_active == False:
            cron.is_active=True
            cron.status='Activado'
            cron.save()
            subprocess.run(["sudo", "service", "cron", "start"])
            return Response ({
                'message': 'CRON is ACTIVE'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'HUBO UN ERROR AL ACTUALIZAR EL ESTADO DE CRON'
        }, status= status.HTTP_400_BAD_REQUEST)
