# Generated by Django 3.2.3 on 2022-10-16 23:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_alter_documentos_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentos',
            name='fecha_creacion',
            field=models.DateField(verbose_name=datetime.datetime(2022, 10, 16, 20, 31, 50, 202832)),
        ),
    ]
