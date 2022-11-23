from apps.management.cron.views import StatusForCron
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', StatusForCron, basename="cron")

urlpatterns = router.urls