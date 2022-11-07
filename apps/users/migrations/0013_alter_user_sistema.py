# Generated by Django 3.2.3 on 2022-11-07 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0043_alter_plantilla_tablas_config'),
        ('users', '0012_alter_user_sistema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sistema',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.sistema'),
        ),
    ]