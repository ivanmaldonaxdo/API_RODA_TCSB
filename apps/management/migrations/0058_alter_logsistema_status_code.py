# Generated by Django 3.2.3 on 2022-11-21 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0057_alter_logsistema_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsistema',
            name='status_code',
            field=models.PositiveSmallIntegerField(default='codigo', verbose_name='Status Respuesta'),
        ),
    ]