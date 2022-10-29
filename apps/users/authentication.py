from rest_framework.authentication import BaseAuthentication
import jwt
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import User

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Token no valido')

        try:
            payload =jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Permisos expirados')

        user = User.objects.get(id=payload['id'])

        if not user:
            raise AuthenticationFailed('Usuario no encontrado')
        
        if user.is_active == False:
            raise AuthenticationFailed('Usuario deshabilitado, contacte a un administrador')

        return (user, None)