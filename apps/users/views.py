import datetime
 #Libreria que maneja las sesiones de usuario
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.usuarios.serializers import UserSerializer
from django.contrib.auth import login
from rest_framework.generics import GenericAPIView
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.middleware import csrf
from django.conf import settings
from pytz import timezone


class Login(APIView):
    def post(self, request):
        email= request.data.get('email','')
        password = request.data.get('password','')

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'message':'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            raise AuthenticationFailed('Contraseña incorrecta')
        
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
        csrf.get_token(request)
        response.data = {
            'jwt':token,
            'message': 'Inicio de session correcto',
        }
        response.status_code= status.HTTP_202_ACCEPTED
        return response
        
class Logout(GenericAPIView): 
    def post(self, request, *args, **kgwars):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Se ha cerrado su sesion'
        }
        return response


# class TokenAuthentication(APIView):
#     def get(self,request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('Token Invalido')
#         try:
#             payload =jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token Expirado')

#         user= User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)