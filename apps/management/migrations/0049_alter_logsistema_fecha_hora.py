# Generated by Django 3.2.3 on 2022-11-13 03:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0048_logsistema_fecha_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsistema',
            name='fecha_hora',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha y Hora'),
        ),
    ]
