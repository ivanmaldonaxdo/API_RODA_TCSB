from rest_framework.permissions import BasePermission


class IsOperador(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:#Validacion que el usuario no es un usuario anonimo
            return request.user.is_staff == True or request.user.role.id == 2


class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:#Validacion que el usuario no es un usuario anonimo
            return request.user.is_staff == True or request.user.role.id == 1
        