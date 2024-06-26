# Generated by Django 5.0.3 on 2024-03-27 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'verbose_name': 'Склад', 'verbose_name_plural': 'Склады'},
        ),
        migrations.AlterField(
            model_name='stock',
            name='occupancy_status',
            field=models.FloatField(default=0, verbose_name='Заполниность стиложей'),
        ),
    ]
