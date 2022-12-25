import logging
import os
import json
import re
import time

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt,csrf_protect  #csrf_exempt局部禁用  csrf_protect启用/
from threading import Thread


from app import models
from backend import settings
from util.grabData_cls import erp_stock
from util.mycls import MyResponse,Myfunction
from util.dy_count_cls import dySales
from util.pdd_count_cls import pdd_tb1
from util.myredis import RedisClient
from conf.exts import *
from conf.functons2 import *

sql_lg=logging.getLogger('sql_log')
#序列化器
class pddSalesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True,required=False)
    shop = serializers.CharField(max_length=64)
    now_date = serializers.DateField()
    deal_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    refund_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    dd_scene = serializers.DecimalField(max_digits=20, decimal_places=2)
    dd_search = serializers.DecimalField(max_digits=20, decimal_places=2)
    fxt = serializers.DecimalField(max_digits=20, decimal_places=2)
    qztg = serializers.DecimalField(max_digits=20, decimal_places=2)
    budan_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    budan_yongjin = serializers.DecimalField(max_digits=20, decimal_places=2)
    is_delete = serializers.IntegerField(default=0, required=False, write_only=True)  # 1=已删除 0=未删除

#ViewSet
class pddSalesViewSet(APIView):
    #查询所有
    def get(self,request):
        request_data = request.GET.dict()
        res = MyResponse()
        try:
            parameters = {}
            if 'shop' in request_data and request_data['shop'] != None and request_data['shop'] != "":
                parameters['shop__in'] = request_data['shop'].split(",")
            if 'start_time' in request_data and request_data['start_time'] != None:
                parameters['now_date__gte'] = request_data['start_time']
            else:
                parameters['now_date__gte'] = "1999-07-13"
            if 'end_time' in request_data and request_data['end_time'] != None:
                parameters['now_date__lte'] = request_data['end_time']
            else:
                parameters['now_date__lte'] = "2098-07-13"
            parameters['is_delete'] = 0

            def myfun(obj_dict, res_list):
                cur_pdd_cls = pdd_tb1(sales_dict=obj_dict)
                cur_pdd_cls.new_data()
                res_list.append(cur_pdd_cls.get_dict)

            obj = models.pdd_sales.objects.filter(**parameters).all().order_by('-now_date')
            obj_ser = pddSalesSerializer(instance=obj, many=True)
            res.is_ok(obj_ser.data)#给返回类 赋值data 并且修改成功状态

            temp_data = obj_ser.data  # 将查询数据取出 暂时存储

            ##线程
            index = 0
            return_list = []
            while True:
                task = []
                for i in range(30):
                    if index >= len(temp_data):
                        break
                    ts = Thread(target=myfun, args=(temp_data[index], return_list))
                    task.append(ts)
                    index += 1
                for i in task:
                    i.start()
                for i in task:
                    i.join()
                if index >= len(temp_data):
                    break

            res.data=return_list
            # for i in range(len(res.data)):#循环返回类的data属性 循环新增计算的值
            #     ds=pdd_tb1(res.data[i])#实例化dysales计算类
            #     ds.new_data()#执行计算方法
            #     res.data[i]=ds.get_dict#将实例化的 dysales计算类 计算之后的新对象进行字典形式赋值给当前循环项的data变量中

            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98, msg=e, data={})
            return Response(res.get_dict)

@api_view(['GET'])
def pdd_get_date_status(request):
    res=MyResponse()
    request_date=request.GET.dict()
    # print(request_date)
    if "date" not in request_date:
        res.need_parameter_err()
        return Response(res.get_dict)

    #创建redis连接
    try:
        rds=RedisClient()
        cur_date_number=request_date['date'].replace("-","")
        bitname="pdd_date_status"#拼多多日报数据流程情况
        status_number=0#此天数据流程状态 0=一步都还没执行 一共5步
        for i in range(4):
            cur_index=int(cur_date_number+str(i+1))
            cur_number=rds.client.getbit(bitname,cur_index)
            status_number+=cur_number
        res.is_ok(data=status_number)
    except Exception as e:
        sql_lg.error(msg=f"用户:{request.session['us_info'].User_name} 查询redisPDD数据状态出错 原因: {e}")
        res.change(status=95,msg="数据库操作失败",data={})
    return Response(res.get_dict)

@api_view(['POST'])
def export_pddday(request):
    res = MyResponse()
    request_date=request.data
    try:
        if 'now_date' not in request.data:
            res.need_parameter_err()
            return Response(res.get_dict)

        obj = models.pdd_sales.objects.filter(now_date=request_date['now_date']).all().order_by('-now_date')

        if obj is None:
            res.none_err()
            return Response(res.get_dict)

        obj_ser = pddSalesSerializer(instance=obj,many=True)
        res.is_ok(obj_ser.data)  # 给返回类 赋值data 并且修改成功状态
        for i in range(len(res.data)):  # 循环返回类的data属性 循环新增计算的值
            ds = pdd_tb1(res.data[i])  # 实例化dysales计算类
            ds.new_data()  # 执行计算方法
            res.data[i] = ds.get_dict  # 将实例化的 dysales计算类 计算之后的新对象进行字典形式赋值给当前循环项的data变量中

        #转成列表形式写入excel
        export_list=[]
        for i in res.data:
            if i['shop']=="PDD女装-IMDAVID禾季纯专卖店":
                i['shop']="PDD女装-I'MDAVID禾季纯专卖店"
            if i['shop']=="PDD女装-IM DAVID小布家":
                i['shop']="PDD女装-I'M DAVID小布家"
            cur_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":60020401, "项目名称":"快递费用", "金额":i['express_price']}
            cur2_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":60020304, "项目名称":"发货费用", "金额":i['deliver_price']}
            cur3_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":60020201, "项目名称":"产品包装耗材", "金额":i['tag_count']}  # 吊牌费
            cur4_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":600503, "项目名称":"吊牌返还", "金额":i['refund_tag_count']}  # 吊牌返还
            cur5_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":600313, "项目名称":"多多搜索+多多推广", "金额":i['dd_scene'] + i['dd_search']}
            cur6_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":600314, "项目名称":"放心推", "金额":i['fxt']}
            cur7_ls = {"店铺名称":i['shop'], "发生日期":i['now_date'], "利润表项目编码":600316, "项目名称":"全站推广", "金额":i['qztg']}
            cur8_ls = {"店铺名称": i['shop'], "发生日期": i['now_date'], "利润表项目编码": 60020403, "项目名称": "补单快递费用", "金额": i['budan_express_price']}
            cur9_ls = {"店铺名称": i['shop'], "发生日期": i['now_date'], "利润表项目编码": 600207, "项目名称": "补单发货费用", "金额": i['budan_deliver_price']}
            cur10_ls = {"店铺名称": i['shop'], "发生日期": i['now_date'], "利润表项目编码": 60030903, "项目名称": "特殊单佣金","金额": i['budan_yongjin']}
            export_list.extend([cur_ls, cur2_ls, cur3_ls, cur4_ls, cur5_ls, cur6_ls, cur7_ls,cur8_ls,cur9_ls,cur10_ls])
        res.data=export_list
        return Response(res.get_dict)
    except Exception as e:
        res.change(status=98, msg=e, data={})
        return Response(res.get_dict)

#修改redis PDD数据 3号状态位
@api_view(['GET'])
def update_date_status(request):
    res=MyResponse()
    request_data=request.GET.dict()
    if 'date' not in request_data:
        res.need_parameter_err()
        return Response(res.get_dict)
    # 创建redis连接
    try:
        rds = RedisClient()
        cur_date_number = request_data['date'].replace("-", "")
        cur_index = int(cur_date_number + str(3))  # 3号位
        bitname = "pdd_date_status"  # 拼多多日报数据流程情况
        rds.client.setbit(name=bitname, offset=cur_index, value=1)
        res.is_ok(data={})
    except Exception as e:
        sql_lg.error(msg=f"用户:{request.session['us_info'].User_name} 修改redisPDD数据状态三号位出错 原因: {e}")
        res.change(status=95,msg="数据库操作失败",data={})
    return Response(res.get_dict)

#获取多维度数据 分析并导入数据库
@api_view(['POST'])
def get_dwd_data(request):
    res=MyResponse()
    request_data = request.data
    us_obj=request.session['us_info']
    es=erp_stock(us_obj.User_erp_cookies)
    #1.从聚水潭抓取聚水潭数据 并保存到服务器
    rs=es.get_dwd_spshop(request_data['date'])
    if not rs['status']:
        res.change(status=98,msg=f"{rs['msg']}请重试或者检查下Cookies更新!",data={})
        return Response(res.get_dict)
    #2.读取本地聚水潭文件分析
    cur_day_path=rs['msg']
    try:
        data_count=read_xlsx_dwd(path=cur_day_path)
    except Exception as e:
        res.change(status=98,msg=f"分析多维度数据失败,原因{e}",data={})
        return Response(res.get_dict)
    #3.存入数据库
    try:
        with transaction.atomic():
            #单线程循环
            for i in data_count:
                cur_i=change_val(i,request_data['date'])#多维度数据 成交金额 与衣服成本需要更换为 主题分析里面得
                cur_shop=cur_i['shop']
                del cur_i['shop']
                for k,y in cur_i.items():
                    defaults_dict={'price':y}
                    cur_name=re.sub('[\u0030-\u0039]',"",k).replace(":","").replace("：","")
                    r=models.pdd_day_record.objects.update_or_create(defaults=defaults_dict,shop=cur_shop,now_date=request_data['date'],name=cur_name)
    except Exception as e:
        logging.getLogger("sql_info").error(f"多维度数据写入数据库失败!已回滚 原因:{e}")
        res.change(status=98,msg="多维度写入数据库失败,已回滚",data={})
        return Response(res.get_dict)
    #上面操作正常完成之后修改redis状态
    try:
        rds = RedisClient()
        cur_date_number = request_data['date'].replace("-", "")
        cur_index = int(cur_date_number + str(4))  # 4号位
        bitname = "pdd_date_status"  # 拼多多日报数据流程情况
        rds.client.setbit(name=bitname, offset=cur_index, value=1)
    except Exception as e:
        sql_lg.error(msg=f"用户:{request.session['us_info'].User_name} 修改redisPDD数据状态四号位出错 原因: {e}")
        res.change(status=95,msg="数据库操作失败",data={})
        return Response(res.get_dict)
    res.change(status=200,msg="多维度数据构建完成!数据库存储完成!",data={})
    return Response(res.get_dict)

#拼多多最终的数据汇总
@api_view(['POST'])
def generate_data_count(request):
    res=MyResponse()
    request_data=request.data

    parameters = {}
    if 'shop' in request_data and request_data['shop'] != None and len(request_data['shop']) != 0:
        parameters['shop__in'] = request_data['shop']
    if 'start_time' in request_data and request_data['start_time'] != None and request_data['start_time'] != "":
        parameters['now_date__gte'] = request_data['start_time']
    else:
        parameters['now_date__gte'] = "1999-07-13"
    if 'end_time' in request_data and request_data['end_time'] != None and request_data['end_time'] != "":
        parameters['now_date__lte'] = request_data['end_time']
    else:
        parameters['now_date__lte'] = "2098-07-13"
    parameters['is_delete'] = 0


    #实例化PDD计算类
    shop_obj_all=models.pdd_sales.objects.filter(**parameters).all()

    def myfun(obj_dict,res_list):
        cur_pdd_cls=pdd_tb1(sales_dict=obj_dict)
        cur_pdd_cls.new2_data()
        res_list.append(cur_pdd_cls.get_dict)
    shop_obj_ser_all=pddSalesSerializer(instance=shop_obj_all,many=True)
    temp_shop_data=shop_obj_ser_all.data#将查询数据取出 暂时存储

    ##线程
    index=0
    return_list=[]
    while True:
        task=[]
        for i in range(50):
            if index >= len(temp_shop_data):
                break
            ts=Thread(target=myfun,args=(temp_shop_data[index],return_list))
            task.append(ts)
            index+=1
        for i in task:
            i.start()
        for i in task:
            i.join()
        if index >= len(temp_shop_data):
            break
    #返回
    res.change(status=200,msg="所有数据计算完成",data=return_list)
    return Response(res.get_dict)

#拼多多所有店铺
@api_view(['GET'])
def get_shop_all(request):
    res=MyResponse()
    try:
        shop_name_all=models.pdd_sales.objects.values("shop")
        shopname_list=[i['shop'] for i in shop_name_all]
        res.change(status=200,msg="获取所有拼多多店铺成功",data=list(set(shopname_list)))
    except Exception as e:
        res.change(status=98,msg=f"获取拼多多所有店铺失败,原因： {e}",data={})
    return Response(res.get_dict)


