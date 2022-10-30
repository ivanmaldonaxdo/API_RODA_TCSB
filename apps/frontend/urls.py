
from django.urls import path
from .views import inicio
from .views import login,homeinfo
urlpatterns = [
    path('home/', inicio, name="inicio"),
    path('loginfront/', login, name="login"),
    path('inicio/', homeinfo, name="homeinfo")
]