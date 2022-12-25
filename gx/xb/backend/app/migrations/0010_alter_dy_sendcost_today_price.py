# Generated by Django 4.0.1 on 2022-10-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_dy_sendcost_refund_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dy_sendcost',
            name='today_price',
            field=models.DecimalField(db_index=True, decimal_places=4, max_digits=20, verbose_name='当天成本价'),
        ),
    ]
