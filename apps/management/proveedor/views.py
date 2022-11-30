from apps.management.proveedor.serializers import ProveedorSerializer, UpdateSerializer
from apps.management.models import Proveedor

from rest_framework.response import Response
from apps.permissions import IsOperador, IsAdministrador, ProveedoresPermission

from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
#Libreria
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots, format_rut_with_dots
from apps.users.authentication import JWTAuthentication

class ProvFilter(FilterSet):
    class Meta:
        model = Proveedor
        fields = {
            'nom_proveedor': ['contains'],
            'rut_proveedor': ['exact'],
        }

class ProveedorViewSets(viewsets.GenericViewSet):
    serializer_class = ProveedorSerializer
    update_serializer_class = UpdateSerializer
    model = Proveedor
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ProvFilter.Meta.fields
    permission_classes= (ProveedoresPermission, )

    def get_queryset(self):
        queryset= self.filter_queryset(Proveedor.objects.all())
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404


    def create(self, request):
        prov_serializer = self.serializer_class(data=request.data)
        if prov_serializer.is_valid():
            prov_serializer.save()
            return Response({
                'message': 'Proveedor registrado correctamente'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro',
            'errors': prov_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None): #Detalle de un usuario
        proveedor  = self.get_object(pk)
        prov_serializer = self.serializer_class(proveedor)
        return Response(prov_serializer.data, status= status.HTTP_200_OK)

    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = ProveedorSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun Proveedor',
            }, status= status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):#Actualizar usuario
        proveedor = self.get_object(pk)
        serializer = self.update_serializer_class(proveedor, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Proveedor actualizado correctamente',
                'Nueva informacion':serializer.data},
                status=status.HTTP_200_OK)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    #Metodo para desactivar o activar clientes, valida el estado en que se encuentra
    #endpoint = 3.219.56.115/proveedores/<pk>/
    def destroy(self, request, pk=None):
        proveedor = self.get_object(pk)
        if proveedor.is_active == True:
            proveedor.is_active=False
            proveedor.save()
            return Response({
                'message': 'Proveedor desactivado'
            }, status=status.HTTP_200_OK)
        elif proveedor.is_active == False:
            proveedor.is_active=True
            proveedor.save()
            return Response({
                'message': 'Proveedor activado'
            }, status=status.HTTP_200_OK)
        return Response({
            'message':'La ID ingresada no coincide con ningun Proveedor'
        }, status= status.HTTP_404_NOT_FOUND)