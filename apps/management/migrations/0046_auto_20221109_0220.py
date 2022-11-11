# Generated by Django 3.2.3 on 2022-11-09 05:20

import apps.management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0045_merge_20221109_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='rut_cliente',
            field=models.CharField(default='Sin Rut', max_length=255, unique=True, validators=[apps.management.models.validar_rut], verbose_name='Rut Cliente'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='rut_proveedor',
            field=models.CharField(max_length=255, unique=True, validators=[apps.management.models.validar_rut], verbose_name='Rut Proveedor'),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='rut_sucursal',
            field=models.CharField(max_length=255, unique=True, validators=[apps.management.models.validar_rut], verbose_name='Rut Sucursal'),
        ),
    ]