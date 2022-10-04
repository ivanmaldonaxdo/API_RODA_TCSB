from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.



#ROLES
class Rol(models.Model):
    role = models.CharField('Rol', max_length=30, default=None, blank=True, null=True)

    def __str__(self):
        return self.role



#USUARIOS
class UserManager(BaseUserManager):
    def _create_user(self, email, name, telefono, role, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email = email,
            name = name,
            telefono = telefono,
            role = role,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, name, telefono, password=None, **extra_fields):
        return self._create_user(email, name, telefono,1, password, False, False, **extra_fields)

    def create_superuser(self, email, name, telefono, role=None , password=None, **extra_fields):
        return self._create_user(email, name, telefono, role,password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombre', max_length = 255, blank = True, null = True)
    telefono = models.CharField('Telefono', max_length= 15, blank=True, null = True)
    role =  models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, default=None)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UserManager()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'telefono']

    def natural_key(self):
        return (self.email)

    def __str__(self):
        return f'{self.name}'   

