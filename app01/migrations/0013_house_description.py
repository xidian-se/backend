# Generated by Django 4.1.3 on 2022-11-15 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_rename_text_house_name_house_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='description',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]