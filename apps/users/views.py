import datetime
from urllib import request
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session #Libreria que maneja las sesiones de usuario
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from apps.users.usuarios.serializers import UserTokenSerializers
from rest_framework.authtoken.models import Token
import pytz
from django.contrib.auth import login




class UserToken(APIView):
    def get(self, request,*args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user =UserTokenSerializers().Meta.model.objects.filter(username = username).first()#validamos que el usuario exista
            )
            return Response({
                'token': user_token.key
            })
        except:
            return Response({
                'error': 'Credenciales incorrectas'
            }, status= status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken): #Esta clase crea una vista normal y define el metodo post
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context = {'request':request})
        #Esta clase ya la definio ObtainAuthToken, requiere el username y password, tambien token.
        if serializer.is_valid():
            user = serializer.validated_data['user']
            usernmae = user.email
            password = user.password
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)#Este metodo crea un token o lo llama si es que ya esta creado
                user_serializer = UserTokenSerializers(user)
                if created:
                    return Response({
                        'message':'Usuario Autenticado',
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email
                        }, status=status.HTTP_200_OK)               
                else:
                    utc_now=datetime.datetime.utcnow()
                    utc_now=utc_now.replace(tzinfo=pytz.utc)
                    all_sessions = Session.objects.filter(expire_date__gte = utc_now)
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'message':'Usuario Autenticado',
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email
                        }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'usuario desactivado'}, status= status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre o usuario incorrecto'}, status= status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:#Hacemos logout si el token del usuario es valido
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now()) #Hace que el sistema desloguee las sessiones que esten a la par de la que inicia sesion
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded() #Si en alguna de las sessiones, se busca el usuario actual y lo encuentra, las borra
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                session_message = 'Sesiones de usuario eliminadas.'
                token.delete()
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, status = status.HTTP_200_OK)
            else:
                return Response({'error': 'No se encuentran usuario con estas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'no se ha encontrado token en la peticion'}, status=status.HTTP_409_CONFLICT)