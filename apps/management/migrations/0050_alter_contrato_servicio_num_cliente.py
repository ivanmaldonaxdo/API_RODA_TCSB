# Generated by Django 3.2.3 on 2022-11-18 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0049_alter_logsistema_fecha_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato_servicio',
            name='num_cliente',
            field=models.CharField(default=None, max_length=255, unique=True, verbose_name='Numero Cliente'),
        ),
    ]
