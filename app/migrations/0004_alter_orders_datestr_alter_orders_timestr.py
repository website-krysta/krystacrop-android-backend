# Generated by Django 4.1.2 on 2023-11-02 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_orders_ordersid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='DateStr',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='orders',
            name='TimeStr',
            field=models.CharField(max_length=12),
        ),
    ]
