# Generated by Django 4.0.1 on 2022-10-27 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_pdd_sales_pdd_sendcost_pdd_sendgoods'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pdd_sales',
            options={'verbose_name': 'pdd_日订单数', 'verbose_name_plural': 'pdd_日订单数'},
        ),
        migrations.AlterModelTable(
            name='pdd_sales',
            table='pdd_sales',
        ),
    ]
