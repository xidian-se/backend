# Generated by Django 4.1.3 on 2022-11-16 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0013_house_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='owners',
            new_name='owner',
        ),
    ]
