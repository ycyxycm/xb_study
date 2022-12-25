# Generated by Django 4.0.1 on 2022-10-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_dy_sendgoods_shop_alter_shop_shop_pallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='cookies_all',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.CharField(db_index=True, max_length=64, verbose_name='店铺')),
                ('Shop_pallet', models.CharField(db_index=True, max_length=12, verbose_name='平台名')),
                ('cookies', models.CharField(db_index=True, max_length=400, verbose_name='cookies')),
                ('update_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'cookies存放表',
                'verbose_name_plural': 'cookies存放表',
                'db_table': 'cookies_all',
            },
        ),
    ]