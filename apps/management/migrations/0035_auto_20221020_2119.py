# Generated by Django 3.2.3 on 2022-10-21 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0034_remove_sucursal_proveedor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato_servicio',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='sucursal',
            name='num_cliente',
        ),
        migrations.AddField(
            model_name='contrato_servicio',
            name='num_cliente',
            field=models.IntegerField(default=None, unique=True, verbose_name='Numero Cliente'),
        ),
    ]