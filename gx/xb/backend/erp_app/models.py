from django.db import models

# Create your models here.
class male_stock(models.Model):
    commodity_code=models.CharField(primary_key=True,max_length=64,db_index=True,verbose_name='商品编码')
    style_code=models.CharField(max_length=64,db_index=True,verbose_name='款式编码')
    number=models.IntegerField(db_index=True,verbose_name='数量')

    class Meta:
        db_table = 'erp_male_stock'
        verbose_name = 'erp_男装临时库存'
        verbose_name_plural = verbose_name

class female_stock(models.Model):
    commodity_code=models.CharField(primary_key=True,max_length=64,db_index=True,verbose_name='商品编码')
    style_code=models.CharField(db_index=True,max_length=64,verbose_name='款式编码')
    number=models.IntegerField(db_index=True,verbose_name='数量')

    class Meta:
        db_table = 'erp_female_stock'
        verbose_name = 'erp_女装临时库存'
        verbose_name_plural = verbose_name

