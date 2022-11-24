from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from apps.management.cron.serializers import CronSerializer
import subprocess
from apps.management.models import ConfigCron, Servicio
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

    #http://localhost:8000/cron/actualizar_parametros_cron/
    @action(detail=False, methods=['post'])
    def actualizar_parametros_cron(self, request):
        cron = self.get_queryset()
        serializer = self.serializer_class(cron, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Parametros actualizados correctamente',
                    'Nueva informacion':serializer.data},
                    status=status.HTTP_200_OK)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)

    #http://localhost:8000/cron/info_cron/
    @action(detail=False, methods=['get'])
    def info_cron(self, request): #Detalle de un usuario
        cron = self.get_object(1)
        servicio = Servicio.objects.get(id=cron.cursor)
        siguiente = Servicio.objects.get(id=cron.cursor+1)
        response = Response()
        data = dict()
        cron_serializer = self.serializer_class(cron)
        if cron.status != 'Desactivado' or cron.status !='Terminado o En espera':
            cron_exec = {'Proceso en ejecucion':servicio.servicio}
            data.update(cron_exec)
        proximo = {'Proximo proceso a ejecutar':siguiente.servicio}
        data.update(proximo)
        response.data = data
        response.status_code= status.HTTP_202_ACCEPTED
        return response


    @action(detail=False, methods=['get'])
    def estado_cron(self, request):
        cron  = self.get_object(1)
        if cron.is_active == True:
            cron.is_active=False
            cron.status='Desactivado'
            cron.save()
            return Response ({
                'message': 'CRON is INACTIVE'
            }, status=status.HTTP_200_OK)
        elif cron.is_active == False:
            cron.is_active=True
            cron.status='Activado'
            cron.save()
            return Response ({
                'message': 'CRON is ACTIVE'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'HUBO UN ERROR AL ACTUALIZAR EL ESTADO DE CRON'
        }, status= status.HTTP_400_BAD_REQUEST)

    #http://localhost:8000/cron/verificar_status/
    @action(detail=False, methods=['get'])
    def verificar_status(self, request):
        cron = self.get_object(1)
        response = Response()
        data = dict()
        estatus = {'status':cron.is_active}
        data.update(estatus)
        response.status_code= status.HTTP_202_ACCEPTED
        response.data = data

        return response
    