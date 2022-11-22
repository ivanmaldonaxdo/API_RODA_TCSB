from django.urls import path
from apps.management.Logs.views import LogViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', LogViewSet, basename="Logs del sistema")

urlpatterns = router.urls