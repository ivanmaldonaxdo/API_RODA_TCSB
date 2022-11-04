import datetime
 #Libreria que maneja las sesiones de usuario
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.usuarios.serializers import UserSerializer
from rest_framework.generics import GenericAPIView
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
from pytz import timezone
from django.contrib.auth import authenticate, login, logout


class authUser(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    def post(self, request):
        email= request.data.get('email','')
        password = request.data.get('password','')

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'message':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'message':'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active == False:
            return Response({'message':'Usuario deshabilitado, contacte a un administrador'}, status=status.HTTP_401_UNAUTHORIZED)

        settings_time_zone = timezone(settings.TIME_ZONE)

        tiempo_creacion = datetime.datetime.now(settings_time_zone)
        tiempo_expiracion = datetime.datetime.now(settings_time_zone)+settings.TOKEN_EXPIRED_AFTER

        payload = {
            'id':user.id,
            'exp': tiempo_expiracion,
            'iat': tiempo_creacion
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token,
            'message': 'Usuario autenticado',
        }
        login(request, user)
        response.status_code= status.HTTP_202_ACCEPTED
        return response
        
class Logout(APIView): 
    def get(self, request, *args, **kgwars):
        response = Response()
        response.delete_cookie('jwt')
        logout(request)
        response.status_code= status.HTTP_200_OK
        response.data = {
            'message': 'Se ha cerrado su sesion'
        }
        return response
