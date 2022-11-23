
from rest_framework.response import Response
from apps.management.procesados.serializers import DocumentoSerializer
from apps.management.models import Documento
from rest_framework.response import Response
from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import FilterSet

# class ClienteFilter(FilterSet):
#     class Meta:
#         model = Documento
#         fields = {
#             'nom_cli': ['contains'],
#             'rut_cliente': ['exact'],
#         }


class ProcesadosViewSet(viewsets.GenericViewSet):
    serializer_class = DocumentoSerializer
    model = Documento
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


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
            serializer = DocumentoSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun documento',
            }, status= status.HTTP_404_NOT_FOUND)
    

    
    def create(self, request, *args, **kwargs):
        serializer_class = DocumentoSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None): 
        documento  = self.get_object(pk)
        serializer = self.serializer_class(documento)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
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
    