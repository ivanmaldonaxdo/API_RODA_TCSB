from django.db import models
from django.core.validators import FileExtensionValidator
from solo.models import SingletonModel
from django.utils import timezone



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
    rut_cliente = models.CharField('Rut Cliente', max_length=10, unique=True, default='Sin Rut')
    razon_social = models.CharField('Razon social', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nom_cli
    
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
    rut_proveedor = models.CharField('Rut Proveedor', max_length=255, blank=False, unique = True)
    contacto = models.CharField('Contacto', max_length=255, blank=True)
    is_active = models.BooleanField(default = True)
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.nom_proveedor
    
    class Meta:
        verbose_name_plural = "Proveedores"


class Plantilla(models.Model):
    nom_doc= models.CharField('Nombre Distribuidor', max_length=255, blank=False)
    version = models.CharField('Version plantilla', max_length=255, blank=False)
    queries_config = models.FileField(null=True, validators=[
        FileExtensionValidator(allowed_extensions=['csv'])
    ])
    tablas_config = models.FileField(null=True, validators=[
        FileExtensionValidator(allowed_extensions=['json'])
    ])
    fecha_creacion = models.DateTimeField(default=timezone.now)
    proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE,null=True, default=None)
    



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
    is_active = models.BooleanField(default = True)
    direccion = models.CharField('Direccion', max_length=255)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cod) +' - '+ str(self.nom_sucursal)
    
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
    num_cliente = models.IntegerField('Numero Cliente', default=None, unique=True, blank=False)

    def __str__(self):
        return self.proveedor + ' - '+ str(self.num_cliente)
