# Generated by Django 3.2.3 on 2022-11-21 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0056_alter_logsistema_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsistema',
            name='response',
            field=models.TextField(default='Response'),
        ),
    ]
