from apps.users.models import User
from apps.users.usuarios.serializers import UserSerializer, UpdateSerializer, UserRolSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from apps.permissions import IsOperador, IsAdministrador, IsRodaUser
from rest_framework.decorators import action
from django.http import Http404
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdministrador]
    serializer_class = UserSerializer
    update_serializer = UpdateSerializer
    model = User
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'email']
    filterset_fields = ['is_active']

    
    def get_queryset(self):
        queryset= self.filter_queryset(User.objects.all())
        return queryset


    
    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404


    def authUser(self, email, password):
        user = authenticate( #devuelve un usuario desde la base de datos con los parametros
                username = email,
                password = password
            )
        return user
    


    #http://localhost:8000/usuarios/?search=Carlos
    #http://localhost:8000/usuarios/?is_active=True

    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = UserSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'La busqueda no coincide con ningun usuario',
            }, status= status.HTTP_404_NOT_FOUND)
        
            
    def create(self, request): #Creacion de usuario
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario registrado',
                'email':user_serializer.validated_data['email'],
                'contraseña':user_serializer.validated_data['password']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro, verifique los campos',
            'errors': user_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None): #Detalle de un usuario
        user  = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data, status= status.HTTP_200_OK)
        

    def update(self, request, pk=None):#Actualizar usuario
        user = self.get_object(pk)
        serializer = self.update_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Usuario actualizado correctamente',
                    'Nueva informacion':request.data},
                    status=status.HTTP_200_OK)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None): #Detalle de un usuario
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    #Metodo para activar o desactivar usuarios
    def destroy(self, request, pk=None):
        user = self.get_object(pk)
        if user.is_active == True:
            user.is_active=False
            user.save()
            return Response({
                'message': 'Usuario desactivado',
            }, status=status.HTTP_200_OK)
        elif user.is_active == False:
            user.is_active=True
            user.save()
            return Response({
                'message': 'Usuario activado'
            }, status=status.HTTP_202_ACCEPTED)
        return Response({
            'message':'La ID ingresada no coincide con ningun usuario'
        }, status= status.HTTP_404_NOT_FOUND)
    

class Roles(viewsets.GenericViewSet):
    permission_classes = [IsAdministrador]
    serializer_class = UserRolSerializer

    def get_queryset(self):
        queryset= self.filter_queryset(User.objects.all())
        return queryset

    def get_object(self, pk):
        try:
            return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    
    def retrieve(self, request, pk=None): #Detalle de un usuario
        user = self.get_object(pk)
        user_serializer = UserRolSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    
    def update(self, request, pk=None):#Actualizar rol
        user = self.get_object(pk)
        serializer = UserRolSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Rol actualizado correctamente',
                    'Nueva informacion':request.data},
                    status=status.HTTP_200_OK)
        return Response({
             'message':'Error en la actualizacion',
             'errors': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)
    


    
    
        
        

