# Generated by Django 3.2.3 on 2022-11-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0060_auto_20221124_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configcron',
            name='status',
            field=models.CharField(choices=[('1', 'En espera'), ('2', 'Recopilando DATA'), ('3', 'Procesando DATA'), ('4', 'Finalizando'), ('5', 'Detenido')], default='5', max_length=100, verbose_name='Status'),
        ),
    ]
