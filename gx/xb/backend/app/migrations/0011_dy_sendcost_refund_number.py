# Generated by Django 4.0.1 on 2022-10-26 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_dy_sendcost_today_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='dy_sendcost',
            name='refund_number',
            field=models.IntegerField(db_index=True, default=0, verbose_name='退货数'),
            preserve_default=False,
        ),
    ]
