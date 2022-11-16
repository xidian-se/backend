# Generated by Django 4.1.3 on 2022-11-16 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0017_account_pay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='pay',
        ),
        migrations.RemoveField(
            model_name='house',
            name='price',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='paid',
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.IntegerField()),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.account')),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.house')),
            ],
        ),
    ]
