from django.urls import path
from apps.management.sucursales.views import SucursalesViewSets, Contrato
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', SucursalesViewSets, basename="sucursales")
router.register(r'contratos', Contrato, basename="contratos")
urlpatterns = router.urls