import datetime
 #Libreria que maneja las sesiones de usuario
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
import jwt
from django.conf import settings
from pytz import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout
from rest_framework.decorators import action
from rest_framework import generics
from apps.users.usuarios.serializers import ChangePasswordSerializer



#Funcion que autentica al usuario al momento de iniciar sesion, debe recibir un correo y contraseña
#al autenticarse correctamente setea una cookie con el token generado en el cliente o navegador que se este utilizando.
#Endpoint:
#http://3.239.33.153/auth-user/
class authUser(APIView):

    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

    def post(self, request):
        email= request.data.get('email','').lower()
        password = request.data.get('password','')

        try:
            user = User.objects.get(email=email)
        except:
            return Response({'message':'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    

        if not user.check_password(password):
            return Response({'message':'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.is_active == False:
            return Response({'message':'Usuario deshabilitado, contacte a un administrador'}, status=status.HTTP_401_UNAUTHORIZED)

        settings_time_zone = timezone(settings.TIME_ZONE)

        tiempo_creacion = datetime.datetime.now(settings_time_zone)
        tiempo_expiracion = datetime.datetime.now(settings_time_zone)+settings.TOKEN_EXPIRED_AFTER

        # all_sessions = Session.objects.filter(expire_date__gte = tiempo_creacion)
        # if all_sessions.exists():
        #     for session in all_sessions:
        #         session_data = session.get_decoded()
        #         if user.id == int(session_data.get('_auth_user_id')):
        #             session.delete()
                    
        payload = {
            'id':user.id,
            'exp': tiempo_expiracion,
            'iat': tiempo_creacion
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        #token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode("utf-8")

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token,
            'message': 'Usuario autenticado',
        }

        login(request, user)
        response.status_code= status.HTTP_202_ACCEPTED
        return response

#Funcion para desloguear al usuario, elimina el token y la sesion de usuario
#http://3.239.33.153/logout/
class Logout(APIView): 
    def get(self, request, *args, **kgwars):
        response = Response()
        logout(request)
        response.delete_cookie('jwt')
        response.delete_cookie('rol')
        response.status_code= status.HTTP_200_OK
        response.data = {
            'message': 'Se ha cerrado su sesion'
        }
        return response

#Funcion para verificar el rol de usuario, importante si se quiere hacer validaciones en el front end VER ROLES DEFINIDOS EN LA BD
#http://3.239.33.153/rol_usuario/
class UserRol(APIView):
    def get(self,request):
        rol = request.user.role.id 
        return Response({'Rol': rol}, status=status.HTTP_200_OK)





#Funcion para cambiar la contraseña de un usuario, este debe estar autenticado antes de realizar la accion
#http://3.239.33.153/api/change-password/
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("contraseña_actual")):
                return Response({"contraseña_actual": ["Incorrecta"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("nueva_contraseña"))
            self.object.save()
           
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Contraseña actualizada correctamente',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Otras URLS funciones importantes
#Instaladas con librerias

#Reset Password, se debe ingresar el email para que se valide que corresponda a un usuario, el sistema envia un correo al usuario con el token
#de validacion
#http://3.239.33.153/api/password_reset/


#En esta URL se ingresa el token de confirmacion que se envio por correo, mas especificando la nueva contraseña
#http://3.239.33.153/api/password_reset/confirm/


#Cambio de contraseñas
#Endpoint:
#http://3.239.33.153/api/change-password/
