# Generated by Django 5.0.3 on 2024-05-09 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_salesitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='sales_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sales_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sold',
        ),
    ]
