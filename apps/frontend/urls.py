
from django.urls import path
from .views import login,homeinfo,processDocs,processed

from .views import login,homeinfo,processDocs, test

urlpatterns = [
    path('process/', processDocs, name="process"),
    path('loginfront/', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo"),
    path('processedDocs/', processed, name="processed"),
    path('test/', test, name='test')
]
