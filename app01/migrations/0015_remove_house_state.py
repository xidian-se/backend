# Generated by Django 4.1.3 on 2022-11-16 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_rename_owners_house_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='state',
        ),
    ]