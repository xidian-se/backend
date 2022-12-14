# Generated by Django 4.1.3 on 2022-11-15 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_alter_account_owner_alter_account_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='renting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.house'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='address',
            field=models.CharField(max_length=50),
        ),
    ]
