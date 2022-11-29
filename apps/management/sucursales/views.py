from apps.management.sucursales.serializers import SucursalSerializers, UpdateSerializer, ContratoSerializer, SucursalModelSerializer, ContratoServiciosSerializer
from apps.management.models import Sucursal, Contrato_servicio
from rest_framework import filters
from rest_framework.response import Response
from apps.permissions import IsOperador, IsAdministrador, SucursalPermission, ContractPermission
from rest_framework.decorators import action
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from apps.users.authentication import JWTAuthentication
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots, format_rut_with_dots




class SucursalFilter(FilterSet):
    class Meta:
        model = Sucursal
        fields = {
            'nom_sucursal':['contains'],
            'cod':['exact'],
            'direccion':['contains'],
            'comuna':['exact'],
            'cliente':['exact'] 
        }

class SucursalesViewSets(viewsets.GenericViewSet):
    serializer_class = SucursalSerializers
    update_serializer_class = UpdateSerializer
    model = Sucursal
    filter_backends = [DjangoFilterBackend]
    filterset_fields = SucursalFilter.Meta.fields
    permission_classes = (SucursalPermission, )

    def get_queryset(self):
        queryset= self.filter_queryset(Sucursal.objects.all())
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404


    def create(self, request):
        sucursal_serializer = self.serializer_class(data=request.data)
        if sucursal_serializer.is_valid():
            sucursal_serializer.save()
            return Response({
                'message': 'Sucursal registrada correctamente'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro',
            'errors': sucursal_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None): #Detalle de un usuario
        sucursal  = self.get_object(pk)
        sucursal_serializer = SucursalModelSerializer(sucursal)
        return Response(sucursal_serializer.data, status= status.HTTP_200_OK)

    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = SucursalModelSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ninguna Sucursal',
            }, status= status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):#Actualizar usuario
        sucursal = self.get_object(pk)
        serializer = self.update_serializer_class(sucursal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Sucursal actualizada correctamente'
            }, status=status.HTTP_201_CREATED)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    #Metodo para desactivar o activar clientes, valida el estado en que se encuentra
    #endpoint = localhost:8000/clientes/<pk>/
    def destroy(self, request, pk=None):
        sucursal = self.get_object(pk)
        sucursal.delete()        
        return Response({
            'message': 'Sucursal Eliminada'
        }, status=status.HTTP_200_OK)
        

 

class Contrato(viewsets.GenericViewSet):
    serializer_class = ContratoServiciosSerializer
    model = Contrato_servicio
    permission_classes = (IsAdministrador, )

    def get_queryset(self):
        queryset= self.filter_queryset(Sucursal.objects.all())
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404


    @action(detail=False, methods=['post'])
    def create_contract(self, request):
        contrato_serializer = self.serializer_class(data=request.data)
        if contrato_serializer.is_valid():
            contrato_serializer.save()
            return Response({
                'message': 'Servicio registrado correctamente'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro',
            'errors': contrato_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contrato = self.get_object(pk)
        if contrato.delete():
            return Response({
                'message': 'Contrato Eliminado'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'La ID ingresada no coincide con ningun contrato'
        }, status= status.HTTP_404_NOT_FOUND)
