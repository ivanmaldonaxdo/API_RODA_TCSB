# Generated by Django 3.2.3 on 2022-11-19 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0052_cron'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cron',
            name='activar',
        ),
        migrations.AddField(
            model_name='cron',
            name='desactivar',
            field=models.CharField(default='', max_length=20, verbose_name='activo'),
        ),
    ]
