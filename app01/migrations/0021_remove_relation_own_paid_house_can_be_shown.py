# Generated by Django 4.1.3 on 2022-11-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0020_remove_relation_account_alter_relation_house'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relation',
            name='own_paid',
        ),
        migrations.AddField(
            model_name='house',
            name='can_be_shown',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
