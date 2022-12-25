from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt,csrf_protect  #csrf_exempt局部禁用  csrf_protect启用/
import json
from threading import Thread

from app import models
from util.mycls import MyResponse,Myfunction
from util.dy_count_cls import dySales,dySurvey
from conf.exts import *
from conf.functons2 import *

#序列化器
class dySalesSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)#read_only=True,
    shop = serializers.CharField(max_length=64,required=False)
    now_date = serializers.DateField(required=False)
    deal_price = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    refund_price = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    freight = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    budan_price = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    budan_yongjin = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    extension_price = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    kf_re_price = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)

    send_timeout = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    small_pay = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    collect_timeout = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    fake_send_timeout = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    violation = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    daren_yongjin = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    marketing = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)

    is_delete = serializers.IntegerField(default=0,required=False,write_only=True)  # 1=已删除 0=未删除

    def update(self, instance, validated_data):
        if 'extension_price' in validated_data:
            instance.extension_price=validated_data['extension_price']
        if 'kf_re_price' in validated_data:
            instance.extension_price=validated_data['kf_re_price']
        instance.save()
        return instance

#ViewSet
class dySalesViewSet(APIView):
    #查询所有
    def get(self,request):
        request_data=request.GET.dict()
        res = MyResponse()
        try:
            parameters={}
            if 'shop' in request_data and request_data['shop']!=None and request_data['shop']!="":
                parameters['shop__in'] = request_data['shop'].split(",")
            if 'start_time' in request_data and request_data['start_time']!=None:
                parameters['now_date__gte'] = request_data['start_time']
            if 'end_time' in request_data and request_data['end_time']!=None:
                parameters['now_date__lte'] = request_data['end_time']
            parameters['is_delete']=0
            obj = models.dy_sales.objects.filter(**parameters).all().order_by('-now_date')
            obj_ser = dySalesSerializer(instance=obj, many=True)
            res.is_ok(obj_ser.data)#给返回类 赋值data 并且修改成功状态

            # for i in range(len(res.data)):#循环返回类的data属性 循环新增计算的值
            #     ds=dySales(res.data[i])#实例化dysales计算类
            #     ds.new_date()#执行计算方法
            #     res.data[i]=ds.get_dict#将实例化的 dysales计算类 计算之后的新对象进行字典形式赋值给当前循环项的data变量中

            index=0
            while True:
                task=[]
                for i in range(30):#循环返回类的data属性 循环新增计算的值
                    if index >= len(res.data):
                        break
                    t=Thread(target=dy_count_function,args=(index,res.data))
                    task.append(t)
                    index+=1
                for i in task:
                    i.start()
                for i in task:
                    i.join()
                if index >= len(res.data):
                    break
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98, msg=e, data={})
            return Response(res.get_dict)

class dySalesViewSetFilter(APIView):
    def put(self,request,id):
        res=MyResponse()
        obj=models.dy_sales.objects.get(id=id)
        if obj is None:
            res.none_err()
            return Response(res.get_dict)
        obj_ser = dySalesSerializer(instance=obj, data=request.data)
        # print(request.data)
        if not obj_ser.is_valid():
            res.check_err(obj_ser.errors)
            return Response(res.get_dict)
        else:
            obj_ser.save()
            res.is_ok(obj_ser.data)
            cls=dySales(res.data)
            cls.new_date()
            res.data=cls.get_dict
            return Response(res.get_dict)


#抖音概况
@api_view(['GET'])
def show_dy_suery(request):
    res=MyResponse()
    request_data = request.GET.dict()
    # print(request_data)
    if 'start_date' in request_data and request_data['start_date'] != None and 'end_date' in request_data and request_data['end_date'] != None:
        now_date_dict = {"start_date":request_data['start_date'],"end_date":request_data['end_date']}#
    else:
        now_date_dict = get_now_yearsmonth()
    # print(now_date_dict)
    #模型类查询参数
    parameters = {}
    if 'shop' in request_data and request_data['shop'] != None and request_data['shop']!="":
        parameters['Shop_name'] = request_data['shop']
    parameters['Shop_pallet'] = '抖音'

    all_dict=[]
    shop_all=models.Shop.objects.filter(**parameters).all()
    # for i in shop_all:
    #     ds=dySurvey(i.Shop_name,start_date=now_date_dict['start_date'],end_date=now_date_dict['end_date'])
    #     all_dict.append(ds.get_dict)
    #多线程查询
    task=[]
    for i in shop_all:
        t=Thread(target=dy_suery_count_function,args=(i.Shop_name,now_date_dict['start_date'],now_date_dict['end_date'],all_dict))
        task.append(t)
    for i in task:
        i.start()
    for i in task:
        i.join()

    res.is_ok(data=all_dict)
    return Response(res.get_dict)