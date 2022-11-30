from random import choices
from secrets import choice
from django.db import models
from apps.management.models import Sistema
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token
from rest_framework import serializers
# Create your models here.


#USUARIOS
class UserManager(BaseUserManager):
    def _create_user(self, email, name, telefono, role, sistema, master, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email = email,
            name = name,
            telefono = telefono,
            role = role,
            sistema = sistema,
            master = master,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, name, telefono, role, sistema, master, password=None, **extra_fields):
        return self._create_user(email, name, telefono, role, sistema,  master, password, False, False, **extra_fields)

    def create_superuser(self, email, name, telefono, role=None, master = None, sistema=None, password=None, **extra_fields):
        return self._create_user(email, name, telefono, role, master, sistema, password, True, True, **extra_fields)


#ROLES
class Rol(models.Model):
    
    role = models.CharField('Rol', max_length=30)

    def __str__(self):
        return self.role
    
    class Meta:
        verbose_name_plural = "Roles de usuario"



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombre', max_length = 255, blank = True, null = True)
    telefono = models.CharField('Telefono', max_length= 15, blank=True, null = True)
    role =  models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, default=None)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, default=1, null=True)
    ESTADOS = (
        (True, 'Activado'),
        (False, 'Desactivado'),
    )
    is_active = models.BooleanField(default = True, choices=ESTADOS)
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

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)




from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message ="Ingrese al link: http://3.239.229.60/api/password_reset/confirm/ y pegue el siguiente codigo con su nueva contraseña token={}".format(reset_password_token.key)
    

    send_mail(
        # title:
        "Recuperar contraseña {title}".format(title="Transcriptor RODA"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )