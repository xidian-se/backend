# Generated by Django 4.1.3 on 2022-11-13 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_owner_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='address',
        ),
        migrations.DeleteModel(
            name='House',
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
        migrations.DeleteModel(
            name='Tenant',
        ),
    ]
