# Generated by Django 3.2.3 on 2022-11-25 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_master'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='master',
        ),
    ]