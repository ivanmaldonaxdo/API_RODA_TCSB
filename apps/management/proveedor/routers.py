from django.urls import path
from apps.management.proveedor.views import ProveedorViewSets
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', ProveedorViewSets, basename="proveedor")

urlpatterns = router.urls