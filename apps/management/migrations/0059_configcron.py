# Generated by Django 3.2.3 on 2022-11-22 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0058_alter_logsistema_status_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigCron',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cursor', models.IntegerField(default=0, verbose_name='Cursor')),
                ('is_active', models.BooleanField(choices=[(True, 'Activado'), (False, 'Desactivado')], default=True)),
                ('hora_gas', models.TimeField(default='14:00')),
                ('hora_agua', models.TimeField(default='08:00')),
                ('hora_luz', models.TimeField(default='02:00')),
            ],
            options={
                'verbose_name': 'Configuracion de CRON',
            },
        ),
    ]