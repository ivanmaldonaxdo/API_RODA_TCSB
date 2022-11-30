from apps.management.clientes.serializers import ClienteSerializer, UpdateSerializer
from apps.management.models import Cliente
from rest_framework import filters
from rest_framework.response import Response
from django.contrib.auth import authenticate
from apps.permissions import ClientesPermission
from rest_framework.decorators import permission_classes, action
from django.http import Http404
import subprocess
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
#Libreria
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots, format_rut_with_dots
from apps.users.authentication import JWTAuthentication

class ClienteFilter(FilterSet):
    class Meta:
        model = Cliente
        fields = {
            'nom_cli': ['contains'],
            'rut_cliente': ['exact'],
        }

class ClienteViewSets(viewsets.GenericViewSet):
    
    serializer_class = ClienteSerializer
    update_serializer_class = UpdateSerializer
    model = Cliente
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ClienteFilter.Meta.fields
    permission_classes = (ClientesPermission,)

    def get_queryset(self):
        queryset= self.filter_queryset(Cliente.objects.all())
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404


    def create(self, request):
        client_serializer = self.serializer_class(data=request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response({
                'message': 'Cliente registrado correctamente'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro',
            'errors': client_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk = None): #Detalle de un usuario
        cliente  = self.get_object(pk)
        cliente_serializer = self.serializer_class(cliente)
        return Response(cliente_serializer.data, status= status.HTTP_200_OK)

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
            serializer.save()
            return Response({'message':'Cliente actualizado correctamente',
                'Nueva informacion':serializer.data},
                status=status.HTTP_200_OK)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    #Metodo para desactivar o activar clientes, valida el estado en que se encuentra
    #endpoint = 100.27.17.66/clientes/7/
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