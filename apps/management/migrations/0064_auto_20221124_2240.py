# Generated by Django 3.2.3 on 2022-11-25 01:40

import apps.management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0063_alter_configcron_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configcron',
            name='cursor',
        ),
        migrations.AlterField(
            model_name='configcron',
            name='status',
            field=models.CharField(choices=[(1, 'En espera'), (2, 'Recopilando DATA'), (3, 'Procesando DATA'), (4, 'Finalizando'), (5, 'Detenido')], default=5, max_length=100, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='rut_proveedor',
            field=models.CharField(max_length=255, unique=True, validators=[apps.management.models.validar_rut], verbose_name='Rut Proveedor'),
        ),
    ]