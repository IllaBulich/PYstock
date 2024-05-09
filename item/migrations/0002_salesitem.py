# Generated by Django 5.0.3 on 2024-05-09 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('product', '0009_delete_item'),
        ('warehouses', '0002_alter_stock_options_alter_stock_occupancy_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('purchase_price', models.FloatField(verbose_name='Стоймасть закупки')),
                ('sales_price', models.FloatField(blank=True, null=True, verbose_name='Стоймасть сбыта')),
                ('purchase_date', models.DateField(verbose_name='Дата поступления')),
                ('sales_date', models.DateField(blank=True, null=True, verbose_name='Дата сбыта')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouses.stock')),
            ],
        ),
    ]
