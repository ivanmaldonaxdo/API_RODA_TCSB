from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from apps.management.cron.serializers import CronSerializer
import subprocess
from apps.management.models import ConfigCron

class StatusForCron(viewsets.ModelViewSet):
    serializer_class = CronSerializer
    model = ConfigCron

    def get_queryset(self):
        queryset=ConfigCron.objects.all().first()
        return queryset

    @action(detail=False, methods=['get'])
    def get_cron(self, request):
        cron  = self.get_queryset()
        cron_serializers = self.serializer_class(cron)
        # subprocess.run(["sudo", "service", "cron", "start"])
        return Response(cron_serializers.data, status= status.HTTP_200_OK)