# Generated by Django 3.2.3 on 2022-10-24 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0037_alter_contrato_servicio_sucursal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comuna',
            name='region',
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='comuna',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.comuna'),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provincia', models.CharField(max_length=255, null=True, verbose_name='Provincia')),
                ('region', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='management.region')),
            ],
            options={
                'verbose_name_plural': 'Provincia',
            },
        ),
        migrations.AddField(
            model_name='comuna',
            name='provincia',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='management.provincia'),
        ),
    ]
