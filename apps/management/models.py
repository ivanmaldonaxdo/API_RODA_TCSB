from datetime import datetime
from email.policy import default
from xml.etree.ElementInclude import default_loader
from django.db import models
from django.core.validators import FileExtensionValidator
from solo.models import SingletonModel
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from apps.management.storage import OverwriteStorage
from rut_chile.rut_chile import is_valid_rut, format_rut_without_dots
from rest_framework import serializers

def validar_rut(value):
    rut_validado = is_valid_rut(value)
    if rut_validado == True:
        return value
    else:
        raise serializers.ValidationError("El rut no es valido")



#Modelo SISTEMA: Mantiene las cpnfiguraciones basicas, tales como, urls, credenciales de las herramientas (Aun necesita modificaciones)
#Solo admite 1 objecto del tipo sistema
class Sistema(SingletonModel):
    singleton_instance_id = 1
    name_sis = models.CharField('Nombre de Sistema',max_length=255,unique = True, blank = True)
    credencial = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['json'])
    ])

    def __str__(self):
        return "Sistema"

    class Meta:
        verbose_name = "Configuracion del sistema"


class Cliente(models.Model):
    nom_cli = models.CharField('Nombre cliente', max_length=255, blank=True, null=True)
    rut_cliente = models.CharField('Rut Cliente', max_length=255, unique=True, default='Sin Rut', validators=[validar_rut])
    razon_social = models.CharField('Razon social', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nom_cli
    
    def save(self, *args, **kwargs):
        self.rut_cliente = format_rut_without_dots(self.rut_cliente)
        super(Cliente, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Clientes"

class Servicio(models.Model):
    servicio= models.CharField('Servicio', max_length=255, blank=False, null=True)

    def __str__(self):
        return self.servicio
    
    class Meta:
        verbose_name_plural = "Servicios"

class Proveedor(models.Model):
    nom_proveedor = models.CharField('Nombre Distribuidor', max_length=255, blank=False)
    rut_proveedor = models.CharField('Rut Proveedor', max_length=255, blank=False, unique = True, validators=[validar_rut])
    contacto = models.CharField('Contacto', max_length=255, blank=True)
    is_active = models.BooleanField(default = True)
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.nom_proveedor
    
    def save(self, *args, **kwargs):
        self.rut_proveedor = format_rut_without_dots(self.rut_proveedor)
        super(Proveedor, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name_plural = "Proveedores"


class Plantilla(models.Model):
    nom_doc= models.CharField('Nombre Distribuidor', max_length=255, blank=False)
    version = models.CharField('Version plantilla', max_length=255, blank=False)
    queries_config = models.FileField(null=True, storage=OverwriteStorage(), validators=[
        FileExtensionValidator(allowed_extensions=['csv','json'])
    ])
    tablas_config = models.FileField(null=True, storage=OverwriteStorage(), validators=[
        FileExtensionValidator(allowed_extensions=['json'])
    ])
    fecha_creacion = models.DateTimeField(default=timezone.now)
    proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE,null=True, default=None)
    
    def __str__(self):
        return self.nom_doc


class Zona(models.Model):
    zona= models.CharField('Zona', max_length=255, blank=False, null=True)

    def __str__(self):
        return self.zona
    
    class Meta:
        verbose_name_plural = "Zonas"

class Region(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, default=None)
    region= models.CharField('Region', max_length=255, blank=False, null=True)

    def __str__(self):
        return self.region
    
    class Meta:
        verbose_name_plural = "Regiones"
    
class Provincia(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=None)
    provincia = models.CharField('Provincia', max_length=255, blank=False, null=True)

    def __str__(self):
        return self.provincia
    
    class Meta:
        verbose_name_plural = "Provincia"

class Comuna(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, default=None)
    comuna= models.CharField('Comuna', max_length=255, blank=False, null=True)

    def __str__(self):
        return self.comuna


class Sucursal(models.Model):
    nom_sucursal = models.CharField('Nombre Unidad', max_length=255, blank=False, null=True)
    cod =  models.IntegerField('Codigo', blank=False, unique= True)
    rut_sucursal = models.CharField('Rut Sucursal', max_length=255, unique = True, validators=[validar_rut])
    is_active = models.BooleanField(default = True)
    direccion = models.CharField('Direccion', max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cod) +' - '+ str(self.nom_sucursal)

    def save(self, *args, **kwargs):
        self.rut_sucursal = format_rut_without_dots(self.rut_sucursal)
        super(Sucursal, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Sucursales"


#Boleta/Factura
class Documento(models.Model):
    nom_doc = models.CharField('Documento',max_length=255, default='Documento')
    folio = models.CharField('Folio',max_length=255, blank=False)
    fecha_procesado = models.DateTimeField(default=timezone.now)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=None)
    procesado = models.BooleanField(default = False)
    documento = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['json', 'pdf'])
    ])

    def __str__(self):
        return self.nom_doc

class Contrato_servicio(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=None)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default=None)
    num_cliente = models.CharField('Numero Cliente', default=None, unique=True, blank=False,max_length=255)

    def __str__(self):
        return str(self.num_cliente)

        # return self.proveedor + ' - ' + str(self.num_cliente)


class LogSistema(models.Model):
    api=models.CharField('URL',max_length=255, blank=False)
    id_user=models.IntegerField('Id Usuario',  blank=False)
    cliente = models.CharField('Cliente', max_length=255, default='No Aplica')
    payload=models.CharField('Payload',max_length=255, blank=False)
    method=models.CharField('Tipo de peticion',max_length=255, blank=False)
    response=models.TextField()
    status_code=models.PositiveSmallIntegerField('Status Respuesta')
    fecha_hora = models.DateTimeField('Fecha y Hora', default=timezone.now)

    def __str__(self):
        return str(self.id)


