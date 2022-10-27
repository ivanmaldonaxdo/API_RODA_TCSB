from django.urls import path
from apps.OCR.procesamiento.processViews import OpenKMViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', OpenKMViewSet, basename="search_docs")

urlpatterns = router.urls