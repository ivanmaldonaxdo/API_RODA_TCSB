from django.urls import path
from apps.users.usuarios.adminViews import UserViewSet, Roles
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', UserViewSet, basename="users")
router.register(r'roles', Roles, basename="roles")
urlpatterns = router.urls

# urlpatterns = [
#     # path('users/', UserList.as_view(), name='user-list'),
   
    
# ]