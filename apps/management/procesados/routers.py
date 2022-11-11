from apps.management.procesados.views import ProcesadosViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', ProcesadosViewSet, basename="procesados")

urlpatterns = router.urls