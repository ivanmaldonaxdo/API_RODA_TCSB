from django.db import models


#SISTEMA
class Sistema(models.Model):
    credencial = models.CharField('Credencial',max_length=255,unique = True,blank = True)
    name_sis = models.CharField('Nombre de Sistema',max_length=255,unique = True, blank = True)
    url = models.CharField('Url',max_length=255,unique = True, blank = True)

    def __str__(self):
        return f'{self.name_sis}'
