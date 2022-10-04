import email
from rest_framework import generics
from apps.users.models import User
from apps.users.usuarios.serializers import UserSerializer
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status



class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    model=User
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', '=email']

    def get_queryset(self):
        queryset= self.filter_queryset(User.objects.all())
        return queryset

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    
    def list(self, request): #Listado de usuario
        query = self.get_queryset()
        if query    :
            serializer = UserSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:   
            return Response({
                'message':'El dato ingresado no coincide con algun(os) usuario(s)',
            }, status= status.HTTP_404_NOT_FOUND)
    
        
    def retrieve(self, request, pk=None): #Detalle de un usuario
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
        

    
    
        
        

