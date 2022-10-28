from django.urls import path
from apps.management.plantilla.views import PlantillaViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import routers


router = DefaultRouter()

router.register('', PlantillaViewSet, basename="plantillas")

urlpatterns = router.urls