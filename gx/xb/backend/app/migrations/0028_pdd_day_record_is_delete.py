# Generated by Django 4.0.1 on 2022-12-01 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_pdd_day_record_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdd_day_record',
            name='is_delete',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
