from django.urls import path
from apps.users.usuarios.adminViews import UserViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', UserViewSet, basename="users")

urlpatterns = router.urls

# urlpatterns = [
#     # path('users/', UserList.as_view(), name='user-list'),
   
    
# ]