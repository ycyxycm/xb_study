from django.db import models

from system.storage import ImageStorage
#店铺表
class Shop(models.Model):
    Shop_id=models.AutoField(primary_key=True,verbose_name='店铺编号')
    Shop_name=models.CharField(max_length=64,verbose_name='店铺名',db_index=True,unique=True)
    Shop_pallet=models.CharField(max_length=12,verbose_name='平台名',db_index=True)
    is_delete=models.IntegerField(default=0,db_index=True)#1=已删除 0=未删除

    class Meta:
        db_table="app_shop"
        verbose_name = "店铺"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Shop_name

#用户表
class Users(models.Model):
    User_id=models.AutoField(primary_key=True,verbose_name='用户编号',db_index=True)
    User_name=models.CharField(max_length=8,verbose_name='用户名',db_index=True,unique=True)
    User_email=models.CharField(max_length=30,verbose_name='邮箱',db_index=True,unique=True)
    User_password=models.CharField(max_length=200,verbose_name='密码',db_index=True)
    User_face=models.ImageField(
        default='face_img/default_face.JPG',
        upload_to='face_img',
        verbose_name='头像',
        storage=ImageStorage())#图片重写存储方法 重命名写入
    User_erp_cookies=models.CharField(max_length=7000,verbose_name="当前用户聚水潭Cookies",null=True,blank=True,default=None)
    is_delete=models.IntegerField(default=0,db_index=True)#1=已删除 0=未删除

    class Meta:
        db_table='app_users'
        verbose_name='用户'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.User_name

#cookie各个平台
class cookies_all(models.Model):
    Shop = models.CharField(max_length=64, db_index=True, verbose_name='店铺',primary_key=True)
    Shop_pallet = models.CharField(max_length=12, verbose_name='平台名', db_index=True)
    cookies=models.CharField(max_length=10000,verbose_name='cookies',db_index=True)
    update_time=models.DateTimeField()

    class Meta:
        db_table='cookies_all'
        verbose_name='cookies存放表'
        verbose_name_plural=verbose_name


'''
    财务
'''
#财务成本价表
class Finace_Cost(models.Model):
    stylecode=models.CharField(primary_key=True,max_length=32,db_index=True,verbose_name='款式编码')
    dy_cost=models.DecimalField(max_digits=20,decimal_places=4,db_index=True,default=0,verbose_name='抖音成本价')
    tm_cost=models.DecimalField(max_digits=20,decimal_places=4,db_index=True,default=0,verbose_name='天猫成本价')
    pdd_cost=models.DecimalField(max_digits=20,decimal_places=4,db_index=True,default=0,verbose_name='拼多多成本价')
    jd_cost=models.DecimalField(max_digits=20,decimal_places=4,db_index=True,default=0,verbose_name='京东成本价')
    tgc_cost = models.DecimalField(max_digits=20, decimal_places=4, db_index=True,default=0,verbose_name='淘工厂成本价')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'Finace_Cost'
        verbose_name = '成本价'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.stylecode

#吊牌价
class finace_tag_price(models.Model):
    shop=models.CharField(max_length=64,db_index=True,verbose_name='店铺',primary_key=True)
    male_tag=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='男装吊牌价')
    female_tag=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='女装吊牌价')
    child_tag=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='童装成本价')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'finace_tag_price'
        verbose_name = '吊牌价表'
        verbose_name_plural = verbose_name

'''
    抖音
'''
#抖音发货 退货数 及当天成本价
class dy_sendcost(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='sendcost编号', db_index=True)
    # shop=models.ForeignKey(to='Shop',on_delete=models.CASCADE,verbose_name='店铺', db_index=True)#关联店铺表
    shop=models.CharField(max_length=64,db_index=True,verbose_name='店铺')
    now_date=models.DateField(verbose_name='日期', db_index=True)
    # stylecode=models.ForeignKey(to='Finace_Cost',on_delete=models.CASCADE,verbose_name='款式编码', db_index=True)
    stylecode=models.CharField(max_length=32,db_index=True,verbose_name='款式编码')
    send_number=models.IntegerField(verbose_name='发货数', db_index=True,default=0)
    refund_number=models.IntegerField(verbose_name='退货数', db_index=True)
    today_price=models.DecimalField(max_digits=20,decimal_places=4,db_index=True,verbose_name='当天成本价')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'dy_sendcost'
        verbose_name = 'dy_发货退货数'
        verbose_name_plural = verbose_name

#抖音订单数
class dy_sendgoods(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='sendgoods编号', db_index=True)
    shop = models.CharField(max_length=64, db_index=True, verbose_name='店铺')
    now_date = models.DateField(verbose_name='日期', db_index=True)
    order_number=models.IntegerField(verbose_name='订单数', db_index=True)
    send_refund_cost=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='发货后退款成本')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'dy_sendgoods'
        verbose_name = 'dy_日订单数'
        verbose_name_plural = verbose_name

#抖音汇总表
class dy_sales(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='sales编号', db_index=True)
    shop = models.CharField(max_length=64,db_index=True, verbose_name='店铺')
    now_date = models.DateField(verbose_name='日期', db_index=True)
    deal_price=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='成交金额')
    refund_price=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='退款金额')
    budan_price=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='补单金额')
    budan_yongjin=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='补单佣金')
    extension_price=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='推广费用')
    kf_re_price=models.DecimalField(max_digits=20,decimal_places=2,db_index=True,verbose_name='客服返现')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    freight = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='运费险')
    send_timeout = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='发货超时')
    collect_timeout = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='揽收超时')
    fake_send_timeout = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='虚假发货超时')
    violation = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='违规')
    small_pay = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='小额打款')
    daren_yongjin = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='达人带货佣金')
    marketing = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='营销费用划扣')



    class Meta:
        db_table = 'dy_sales'
        verbose_name = 'dy_汇总表'
        verbose_name_plural = verbose_name

'''
    拼多多
'''
#拼多多 发货 退货数 当天成本价 当天吊牌价
class pdd_sendcost(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='sendcost编号', db_index=True)
    shop = models.CharField(max_length=64, db_index=True, verbose_name='店铺')
    now_date = models.DateField(verbose_name='日期', db_index=True)
    stylecode = models.CharField(max_length=32, db_index=True, verbose_name='款式编码')
    send_number = models.IntegerField(verbose_name='发货数', db_index=True, default=0)
    refund_number = models.IntegerField(verbose_name='退货数', db_index=True)
    today_price = models.DecimalField(max_digits=20, decimal_places=4, db_index=True, verbose_name='当天成本价')
    today_tag = models.DecimalField(max_digits=20, decimal_places=4, db_index=True, verbose_name='当天吊牌价')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'pdd_sendcost'
        verbose_name = 'pdd_发货退货数'
        verbose_name_plural = verbose_name

#拼多多 订单数
class pdd_sendgoods(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='sendgoods编号', db_index=True)
    shop = models.CharField(max_length=64, db_index=True, verbose_name='店铺')
    now_date = models.DateField(verbose_name='日期', db_index=True)
    order_number=models.IntegerField(verbose_name='订单数', db_index=True)
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'pdd_sendgoods'
        verbose_name = 'pdd_日订单数'
        verbose_name_plural = verbose_name

#拼多多 日常记账
class pdd_day_record(models.Model):
    shop = models.CharField(max_length=64, db_index=True, verbose_name='店铺')
    now_date = models.DateField(verbose_name='日期', db_index=True)
    name=models.CharField(max_length=64, db_index=True, verbose_name='名称')
    price=models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='名称金额')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'pdd_day_record'
        unique_together=(("shop","now_date",'name'))
        verbose_name = 'pdd_日常记账'
        verbose_name_plural = verbose_name

#拼多多 汇总表
class pdd_sales(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='sales编号', db_index=True)
    shop = models.CharField(max_length=64, db_index=True, verbose_name='店铺')
    now_date = models.DateField(verbose_name='日期', db_index=True)
    deal_price = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='成交金额')
    refund_price = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='退款金额')
    dd_scene=models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='多多场景')
    dd_search=models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='多多搜索')
    fxt=models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='放心推')
    qztg=models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='全站推广')
    budan_price=models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='补单金额')
    budan_yongjin = models.DecimalField(max_digits=20, decimal_places=2, db_index=True, verbose_name='补单佣金')
    is_delete = models.IntegerField(default=0, db_index=True)  # 1=已删除 0=未删除

    class Meta:
        db_table = 'pdd_sales'
        verbose_name = 'pdd_日订单数'
        verbose_name_plural = verbose_name