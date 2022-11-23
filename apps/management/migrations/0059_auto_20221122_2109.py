# Generated by Django 3.2.3 on 2022-11-23 00:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0058_alter_logsistema_status_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='sucursal',
        ),
        migrations.AddField(
            model_name='documento',
            name='contrato_servicio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.contrato_servicio'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='documento',
            field=models.FileField(upload_to='procesados/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['json', 'pdf'])]),
        ),
    ]
