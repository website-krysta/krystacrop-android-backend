# Generated by Django 4.1.2 on 2023-11-06 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_orders_datestr_alter_orders_timestr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='DateStr',
            field=models.DateField(),
        ),
    ]