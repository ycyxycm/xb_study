# Generated by Django 4.1.1 on 2022-10-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_shop_shop_pallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='dy_sendgoods',
            name='shop',
            field=models.CharField(db_index=True, default='a', max_length=64, verbose_name='店铺'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='Shop_pallet',
            field=models.CharField(db_index=True, max_length=12, verbose_name='平台名'),
        ),
    ]
