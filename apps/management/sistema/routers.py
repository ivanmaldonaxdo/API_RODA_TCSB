from django.urls import path
from apps.management.sistema.views import SistemaViewSets
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', SistemaViewSets, basename="sistema")

urlpatterns = router.urls