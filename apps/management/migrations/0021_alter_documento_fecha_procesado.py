# Generated by Django 3.2.3 on 2022-10-19 03:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_alter_documento_fecha_procesado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='fecha_procesado',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 19, 0, 20, 7, 742533)),
        ),
    ]
