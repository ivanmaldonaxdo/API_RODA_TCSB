from apps.management.clientes.serializers import ClienteSerializer, UpdateSerializer
from apps.management.models import Cliente

from rest_framework import filters
from rest_framework.response import Response
from django.contrib.auth import authenticate
from apps.permissions import IsOperador, IsAdministrador
from rest_framework.decorators import action


from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

#Libreria
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots


class ClienteViewSets(viewsets.GenericViewSet):
    serializer_class = ClienteSerializer
    update_serializer_class = UpdateSerializer
    model = Cliente
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom_cli', 'rut_cliente']

    def get_queryset(self):
        queryset= self.filter_queryset(Cliente.objects.all())
        return queryset

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)


    def create(self, request):
        client_serializer = self.serializer_class(data=request.data)
        if client_serializer.is_valid():
            rut = client_serializer.validated_data.get('rut_cliente')
            rut = format_rut_without_dots(rut)
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

    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = ClienteSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun cliente',
            }, status= status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):#Actualizar usuario
        cliente = self.get_object(pk)
        serializer = self.update_serializer_class(cliente, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            rut = serializer.validated_data.get('rut_cliente')
            rut = format_rut_without_dots(rut)
            if len(rut)<=10 and is_valid_rut(rut):
                serializer.save()
                return Response({'message':'Cliente actualizado correctamente',
                    'Nueva informacion':serializer.data},
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    'message':'El rut ingresado no es valido',
                }, status= status.HTTP_400_BAD_REQUEST)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    #Metodo para desactivar o activar clientes, valida el estado en que se encuentra
    #endpoint = localhost:8000/clientes/7/
    def destroy(self, request, pk=None):
        cliente = self.get_object(pk)
        if cliente.is_active == True:
            cliente.is_active=False
            cliente.save()
            return Response({
                'message': 'Cliente desactivado'
            }, status=status.HTTP_200_OK)
        elif cliente.is_active == False:
            cliente.is_active=True
            cliente.save()
            return Response({
                'message': 'Cliente activado'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'La ID ingresada no coincide con ningun usuario'
        }, status= status.HTTP_404_NOT_FOUND)