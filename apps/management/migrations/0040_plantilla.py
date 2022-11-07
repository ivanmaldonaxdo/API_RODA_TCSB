# Generated by Django 3.2.3 on 2022-11-02 23:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0039_auto_20221102_0048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plantilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_doc', models.CharField(max_length=255, verbose_name='Nombre Distribuidor')),
                ('version', models.CharField(max_length=255, verbose_name='Version plantilla')),
                ('queries_config', models.FileField(null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('tablas_config', models.FileField(null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('proveedor', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.proveedor')),
            ],
        ),
    ]