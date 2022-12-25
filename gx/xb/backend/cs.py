from django.db.models import Sum, F

import os
import django
os.environ.setdefault("DJANGO_SETTING_MODULE",'backend.settings')
django.setup()
from app import models
#拼多多替换掉多维度导出数据中的部分字段值


def chengfa(a,b):
    return a*b



# category = Category.objects.first()  # 选出第一个分类
# all_details = DetailsPrice.objects.filter(design=category)  # 筛选出所有的 产品
# # todo 算出 unit_price 不为空的所有产品的总价值
# all_cost = all_details.filter(unit_price__isnull=False).aggregate(all_cost=Sum(F("num") * F("unit_price"), output_field=models.DecimalField(max_digits=15, decimal_places=2)))
#
# all_cost=all_cost["all_cost"] if all_cost.get("all_cost")



def change_val(dict,date):
    a_list= {}
    pdd_obj=models.pdd_sales.objects.filter(now_date="2022-11-20").all()
    for i in pdd_obj:
        a_list[i.shop]=""
    print(a_list)


    # copy_dict=dict
    # if "付款订单金额" in copy_dict:
    #     pdd_sendcost_filter = models.pdd_sendcost.objects.filter(shop=copy_dict['shop'], now_date=date).all().



        # copy_dict['付款订单金额']
#
if __name__=='__main__':
    pass