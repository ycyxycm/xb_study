# Generated by Django 4.0.1 on 2022-11-11 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_dy_sales_collect_timeout_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='User_erp_cookies',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='当前用户聚水潭Cookies'),
        ),
    ]
