from apps.management.procesados.views import ProcesadosViewSet, DownloadViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()

router.register('', ProcesadosViewSet, basename="procesados")
router.register(r'download', DownloadViewSet, basename="download")
urlpatterns =router.urls