from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message':'Usuario Autenticado',
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'error':'El usuario no se encuentra activo'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error':'Las credenciales no son validas'}, status=status.HTTP_404_NOT_FOUND)

