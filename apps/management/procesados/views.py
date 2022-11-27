from rest_framework import filters
from rest_framework.response import Response
from apps.management.procesados.serializers import DocumentosSerializers,ContratoSerializer
from apps.management.models import Documento,Contrato_servicio
from rest_framework.response import Response
from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import FilterSet
from django_filters import FilterSet, AllValuesFilter, DateTimeFilter, NumberFilter ,DateFromToRangeFilter,ChoiceFilter
# import django_filters
from apps.permissions import  *
# from django_filters import FilterSet

class DocumentoFilter(FilterSet):
    # sucursal = ChoiceFilter(field_name = 'contrato_servicio__sucursal')
    class Meta:
        model = Documento
        fields = {
                'folio':['exact'],
                'contrato_servicio__proveedor':['exact'],
                'contrato_servicio__sucursal':['exact'],
                'contrato_servicio__sucursal__cliente':['exact'],
                'fecha_procesado':['date']

            }


class ProcesadosViewSet(viewsets.GenericViewSet):
    serializer_class = DocumentosSerializers
    model = Documento
    # filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = DocumentoFilter.Meta.fields
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['fecha_procesado']
    permission_classes = (ProcesadosPermission,)


    def get_queryset(self):
        queryset= self.filter_queryset(Documento.objects.all().order_by('-fecha_procesado'))
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404


    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = DocumentosSerializers(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)
    

    
    # def create(self, request, *args, **kwargs):
    #     serializer_class = DocumentoSerializer(data=request.data)
    #     if serializer_class.is_valid():
    #         serializer_class.save()
    #         return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None): 
        documento  = self.get_object(pk)
        serializer = self.serializer_class(documento)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def destroy(self, request, pk = None): 
        documento  = self.get_object(pk)
        folio = documento.folio
        documento.delete()
        
        return Response({'message':'documento eliminado'}, status= status.HTTP_200_OK)
    
    # @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    # def download(self, *args, **kwargs):
    #     instance = Documento.objects.get()

    #     # get an open file handle (I'm just using a file attached to the model for this example):
    #     file_handle = instance.file.open()

    #     # send file
    #     response = FileResponse(file_handle, content_type='whatever')
    #     response['Content-Length'] = instance.file.size
    #     response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name

    #     return response
    