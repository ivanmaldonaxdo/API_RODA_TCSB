
from django.urls import path
from .views import login,homeinfo,processDocs,processed,test,cron

urlpatterns = [
    path('process/', processDocs, name="process"),
    path('', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo"),
    path('processedDocs/', processed, name="processed"),
    path('automatizacion/', cron, name="cron"),
    path('test/', test, name='test')
]
