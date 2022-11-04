from apps.management.sistema.serializers import SistemaSerializers
from apps.management.models import Sistema

from rest_framework.response import Response
from apps.permissions import IsAdministrador
from rest_framework.decorators import action
from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status



class SistemaViewSets(viewsets.ModelViewSet):
    serializer_class = SistemaSerializers
    model = Sistema
    permission_classes= (IsAdministrador,)

    def get_queryset(self):
        queryset= Sistema.objects.all().first()
        return queryset

    @action(detail=False, methods=['get'])
    def get_sistema(self, request):
        sis  = self.get_queryset()
        sis_serializer = self.serializer_class(sis)
        return Response(sis_serializer.data, status= status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def actualizar_sistema(self, request):
        sis = self.get_queryset()
        serializer = self.serializer_class(sis, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Parametros actualizados correctamente',
                    'Nueva informacion':serializer.data},
                    status=status.HTTP_200_OK)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)
