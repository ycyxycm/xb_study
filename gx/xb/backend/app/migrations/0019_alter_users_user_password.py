# Generated by Django 4.0.1 on 2022-11-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_dy_sales_plat_cost_dy_sendgoods_send_refund_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='User_password',
            field=models.CharField(db_index=True, max_length=200, verbose_name='密码'),
        ),
    ]
