
from django.urls import path
from .views import login,homeinfo,processDocs

urlpatterns = [
    path('process/', processDocs, name="process"),
    path('loginfront/', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo")
]