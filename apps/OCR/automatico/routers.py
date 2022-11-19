from django.urls import path

from apps.OCR.automatico.cron import procesoautomatico
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('', procesoautomatico, basename="procesocron")
urlpatterns = router.urls