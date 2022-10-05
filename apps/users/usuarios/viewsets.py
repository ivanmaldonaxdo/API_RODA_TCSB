import email
from rest_framework import generics
from apps.users.models import User
from apps.users.usuarios.serializers import UserSerializer, UpdateSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status



class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    update_serializer = UpdateSerializer
    model=User
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', '=email']
    def get_queryset(self):
        queryset= self.filter_queryset(User.objects.all())
        return queryset

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)


    def authUser(self, email, password):
        user = authenticate( #devuelve un usuario desde la base de datos con los parametros
                username = email,
                password = password
            )
        return user
    
    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query:
            serializer = UserSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'El dato ingresado no coincide con algun(os) usuario(s)',
            }, status= status.HTTP_404_NOT_FOUND)

    def create(self, request): #Creacion de usuario
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            email = user_serializer.validated_data['email']
            password = user_serializer.validated_data['password']
            user = self.authUser(email, password)
            token = Token.objects.create(user=user)
            return Response({
                'Token':token.key,
                'message': 'Usuario registrado',
                'email':user_serializer.validated_data['email'],
                'contraseña':user_serializer.validated_data['password']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Error en el registro',
            'errors': user_serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)
        

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
    
    
        
        

