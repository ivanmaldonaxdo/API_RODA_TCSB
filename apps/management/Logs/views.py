from apps.management.models import LogSistema
from apps.management.Logs.serializers import LogSerializer
from rest_framework.response import Response
from apps.permissions import IsAdministrador
from rest_framework.decorators import action
from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class LogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdministrador]
    serializer_class = LogSerializer
    model = LogSistema
    http_method_names = ['get']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return LogSistema.objects.all().order_by('-id')
    
    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    

    @action(detail=True, methods=['get'])
    def log(self, request, pk=None):
        logs  = self.get_object(pk)
        logs_serializer = self.serializer_class(logs)
        return Response(logs_serializer.data, status= status.HTTP_200_OK)