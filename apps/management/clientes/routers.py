from django.urls import path
from apps.management.clientes.views import ClienteViewSets
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', ClienteViewSets, basename="clientes")

urlpatterns = router.urls