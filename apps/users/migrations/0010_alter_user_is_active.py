# Generated by Django 3.2.3 on 2022-10-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_rol_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(choices=[(True, 'Activado'), (False, 'Desactivado')], default=True),
        ),
    ]
