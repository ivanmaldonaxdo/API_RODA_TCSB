# Generated by Django 3.2.3 on 2022-10-19 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_rol_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='role',
            field=models.CharField(default='Sin Rol', max_length=30, verbose_name='Rol'),
        ),
    ]