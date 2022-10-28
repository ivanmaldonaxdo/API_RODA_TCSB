
from rest_framework.response import Response
from yaml import serialize
from .serializers import UpdateSerializer
from apps.management.plantilla.serializers import PlantillaSerializer, UpdateSerializer
from apps.management.models import Plantilla
from rest_framework.response import Response
from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from apps.users.authentication import ExpiringTokenAuthentication
from rest_framework import generics
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from rest_framework.views import APIView
from .serializers import PlantillaSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers

# ViewSets define the view behavior.
class PlantillaViewSet(viewsets.GenericViewSet):
    serializer_class = PlantillaSerializer
    update_serializer_class = UpdateSerializer
    model = Plantilla
    serializer_class = UpdateSerializer

    def get_queryset(self):
        queryset= self.filter_queryset(Plantilla.objects.all())
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = PlantillaSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ninguna plantilla',
            }, status= status.HTTP_404_NOT_FOUND)
    
    def create(self, request, *args, **kwargs):
        serializer_class = PlantillaSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None): #Detalle de una plantilla
        plantilla  = self.get_object(pk)
        prov_serializer = self.serializer_class(plantilla)
        return Response(prov_serializer.data, status= status.HTTP_200_OK)
    
    def update(self, request, pk = None):
        plantilla  = self.get_object(pk)
        serializer = self.update_serializer_class(plantilla, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Plantilla actualizada',
                    'Nueva informacion':serializer.data},
                    status=status.HTTP_200_OK)
        else:
            return Response({
                    'message':'Error al actualizar plantilla',
                }, status= status.HTTP_400_BAD_REQUEST)