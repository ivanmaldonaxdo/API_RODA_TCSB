from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

class IsOperador(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:#Validacion que el usuario no es un usuario anonimo
            return request.user.is_staff == True or request.user.role.id == 2


class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:#Validacion que el usuario no es un usuario anonimo
            return request.user.is_staff == True or request.user.role.id == 1


class IsRodaUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:#Validacion que el usuario no es un usuario anonimo
            return request.user.is_staff == True or request.user.role.id == 3
        
class IsCron(BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:#Validacion que el usuario no es un usuario anonimo
            return request.user.is_staff == True or request.user.email == "usuariocron@gmail.com"
        

class ClientesPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_staff == True or request.user.role.id == 1
        else:
            return False

class ProcesadosPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_staff == True or request.user.role.id == 1
        else:
            return False


class ProcessPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['search_docs','process_docs']:
            return request.user.is_staff == True or request.user.role.id == 1 or request.user.role.id ==2
        else:
            return False

class CronPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['actualizar_parametros_cron', 'info_cron', 'estado_cron', 'verificar_status']:
            return bool(request.user.is_staff or request.user.role == 1 or request.user.role == 2)
        else:
            return False




class SucursalPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_staff == True or request.user.role.id == 1 
        else:
            return False

class ContractPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create_contract', 'destroy']:
            return request.user.is_staff == True or request.user.role.id == 1 or request.user.role.id == 2
        else:
            return False


class ProveedoresPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_staff == True or request.user.role.id == 1
        else:
            return False

class CronPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_staff == True or request.user.role.id == 1
        else:
            return False



# class OpenKMPermission(BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ['list', 'retrieve']:
#             return True
#         elif view.action in ['create', 'update', 'destroy']:
#             return request.user.is_staff == True or request.user.role.id == 1
#         else:
#             return False
                                                                       