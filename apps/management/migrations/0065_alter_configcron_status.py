# Generated by Django 3.2.3 on 2022-11-25 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0064_auto_20221124_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configcron',
            name='status',
            field=models.CharField(choices=[('En espera', 'En espera'), ('Recopilando DATA', 'Recopilando DATA'), ('Procesando DATA', 'Procesando DATA'), ('Finalizando', 'Finalizando'), ('Detenido', 'Detenido')], default='En espera', max_length=100, verbose_name='Status'),
        ),
    ]
