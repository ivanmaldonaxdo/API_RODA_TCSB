# Generated by Django 3.2.3 on 2022-11-08 00:13

import apps.management.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0043_alter_plantilla_tablas_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantilla',
            name='queries_config',
            field=models.FileField(null=True, storage=apps.management.storage.OverwriteStorage(), upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])]),
        ),
        migrations.AlterField(
            model_name='plantilla',
            name='tablas_config',
            field=models.FileField(null=True, storage=apps.management.storage.OverwriteStorage(), upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['json'])]),
        ),
    ]