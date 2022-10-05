from email.policy import default
from django.db import models


#SISTEMA
class Sistema(models.Model):
    credencial = models.CharField('Credencial',max_length=255,unique = True,blank = True)
    name_sis = models.CharField('Nombre de Sistema',max_length=255,unique = True, blank = True)
    url = models.CharField('Url',max_length=255,unique = True, blank = True)



    def __str__(self):
        return f'{self.name_sis}'

class Cliente(models.Model):
    nom_cli = models.CharField('Nombre cliente', max_length=255, blank=True, null=True)
    rut_cliente = models.CharField('Rut Cliente', max_length=255, blank=True, null=True)
    #servicio_contratado = models.CharField('Servicio Contratado', max_length=255, blank=True, null=True)
    razon_social = models.CharField('Razon social', max_length=255, blank=True, null=True)
    direccion_sucursal_cliente = models.CharField('Direccion sucursal', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nom_cli