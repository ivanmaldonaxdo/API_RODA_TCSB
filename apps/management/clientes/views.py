from apps.management.clientes.serializers import ClienteSerializer
from apps.management.models import Cliente

from rest_framework import filters
from rest_framework.response import Response
from django.contrib.auth import authenticate
from apps.permissions import IsOperador, IsAdministrador
from rest_framework.decorators import action


from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots


class ClienteViewSets(viewsets.GenericViewSet):
    serializer_class = ClienteSerializer
    model = Cliente
    filter_backends = [filters.SearchFilter]
    search_fields = ['=nom_cli', '=rut_cliente']

    def create(self, request):
        client_serializer = self.serializer_class(data=request.data)
        if client_serializer.is_valid():
            rut = client_serializer.validated_data.get('rut_cliente')
            rut = format_rut_without_dots(rut)
            print(rut)
            if len(rut)<=10 and is_valid_rut(rut):
                client_serializer.save()
                return Response({
                    'message': 'Cliente registrado correctamente'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message':'El rut ingresado no es valido',
                }, status= status.HTTP_400_BAD_REQUEST)
        return Response({
            'message':'Error en el registro',
            'errors': client_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    