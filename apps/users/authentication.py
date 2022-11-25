from rest_framework.authentication import BaseAuthentication
import jwt
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import User
from django.conf import settings

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Token no valido')
        

        #Autenticacion personalizada para el usuario CRON, modificar el email en caso de modificar el usuario en la BD
        if token == settings.CRON_CREDENCIAL:
            user = User.objects.get(email='usuariocron@gmail.com')
            return (user, None)

        try:
            payload =jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Permisos expirados')

        user = User.objects.get(id=payload['id'])

        if not user:
            raise AuthenticationFailed('Usuario no encontrado')
        
        if user.is_active == False:
            raise AuthenticationFailed('Usuario deshabilitado, contacte a un administrador')

        return (user, None)