import logging

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt,csrf_protect  #csrf_exempt局部禁用  csrf_protect启用/
import json,os

from app import models
from util.mycls import MyResponse,Myfunction
from backend import settings
from conf.exts import *

sql_log=logging.getLogger("sql_log")
#成本价序列化器
class FinaceCostSerializer(serializers.Serializer):
    stylecode = serializers.CharField(max_length=32)
    dy_cost = serializers.DecimalField(max_digits=20, decimal_places=4,required=False)
    tm_cost = serializers.DecimalField(max_digits=20, decimal_places=4,required=False)
    pdd_cost = serializers.DecimalField(max_digits=20, decimal_places=4,required=False)
    jd_cost = serializers.DecimalField(max_digits=20, decimal_places=4,required=False)
    tgc_cost = serializers.DecimalField(max_digits=20, decimal_places=4,required=False)
    is_delete = serializers.IntegerField(default=0,required=False,write_only=True)  # 1=已删除 0=未删除

    #APIView重写create
    def create(self, validated_data):
        instance=models.Finace_Cost.objects.create(
            stylecode=validated_data['stylecode'],
            dy_cost = validated_data['dy_cost'],
            tm_cost = validated_data['tm_cost'],
            pdd_cost = validated_data['pdd_cost'],
            jd_cost = validated_data['jd_cost'],
            tgc_cost = validated_data['tgc_cost']
        )
        return instance

    #APIView重写update
    def update(self, instance, validated_data):
        # if 'stylecode' in validated_data:
        #     instance.stylecode=validated_data['stylecode']
        if 'dy_cost' in validated_data:
            instance.dy_cost = validated_data['dy_cost']
        if 'tm_cost' in validated_data:
            instance.tm_cost = validated_data['tm_cost']
        if 'pdd_cost' in validated_data:
            instance.pdd_cost = validated_data['pdd_cost']
        if 'jd_cost' in validated_data:
            instance.jd_cost = validated_data['jd_cost']
        if 'tgc_cost' in validated_data:
            instance.tgc_cost = validated_data['tgc_cost']
        instance.save()
        return instance

#成本价ViewSet
class FinaceCostViewSet(APIView):
    #get
    def get(self,request):
        res=MyResponse()
        try:
            obj=models.Finace_Cost.objects.all()
            obj_ser=FinaceCostSerializer(instance=obj,many=True)
            res.is_ok_count(obj_ser.data,len(obj_ser.data))
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98,msg=e,data={})
            return Response(res.get_dict)

    #post
    def post(self,request):
        res = MyResponse()  # 实例化myresponse
        myfuct=Myfunction(FinaceCostSerializer)#实例化myfunction
        add_res=myfuct.obj_add(rs_data=request.data)
        res.change(status=add_res['status'], msg=add_res['msg'], data=add_res['data'])
        return Response(res.get_dict)

class FinaceCostViewSetFilter(APIView):
    #get
    def get(self,request):
        res = MyResponse()
        if 'stylecode' not in request.data:
            res.need_parameter_err()
            return Response(res.get_dict)
        try:
            obj = models.Finace_Cost.objects.filter(stylecode=request.data['stylecode']).first()
            if obj is None:
                res.none_err()
                return Response(res.get_dict)
            obj_ser = FinaceCostSerializer(instance=obj)
            res.change(status=200,msg="单个查询成功",data=obj_ser.data)
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98, msg=e, data={})
            return Response(res.get_dict)

    #put
    def put(self,request):
        res = MyResponse()
        if 'stylecode' not in request.data:
            res.need_parameter_err()
            return Response(res.get_dict)
        obj = models.Finace_Cost.objects.filter(stylecode=request.data['stylecode']).first()
        if obj is None:
            res.none_err()
            return Response(res.get_dict)
        obj_ser = FinaceCostSerializer(instance=obj, data=request.data)

        if not obj_ser.is_valid():
            res.check_err(obj_ser.errors)
            return Response(res.get_dict)
        else:
            obj_ser.save()
            res.change(status=200,msg="成本价修改成功!",data=obj_ser.data)
            return Response(res.get_dict)

    #del


@api_view(['POST'])
def import_newCost(request):
    res = MyResponse()

    # 接收上传保存到本地
    file = request.FILES.get('file')
    template_str = f"{request.session['us_info'].User_name}-{get_now_date()}-"
    file_path=os.path.join(settings.MEDIA_ROOT, f'update_cost_files/{template_str}{file.name}')
    with open(file_path, "wb") as z:
        for i in file.chunks():
            z.write(i)

    # 读取上传文件覆盖数据库
    file_data=read_xlsx(path=file_path,header_line=0)
    #判断格式
    if "款式编码" not in file_data[0] or "抖音成本价" not in file_data[0] or "天猫成本价" not in file_data[0] or "拼多多成本价" not in file_data[0] or "京东成本价" not in file_data[0] or "淘工厂成本价" not in file_data[0]:
        res.change(status=98,msg="上传文件模板错误,请参考模板文件",data={})
        return Response(res.get_dict)
    code_index,dy,tm,pdd,jd,tgc=file_data[0].index("款式编码"),file_data[0].index("抖音成本价"),\
                file_data[0].index("天猫成本价"),file_data[0].index("拼多多成本价"),\
                file_data[0].index("京东成本价"),file_data[0].index("淘工厂成本价")

    new_cost={}
    for i in file_data[1:]:
        new_cost[i[code_index]]={}
        if i[dy]!=-1 and i[dy]!=None:
            new_cost[i[code_index]]["dy_cost"]=round(float(i[dy]),4)
        if i[tm]!=-1 and i[tm]!=None:
            new_cost[i[code_index]]["tm_cost"]=round(float(i[tm]),4)
        if i[pdd]!=-1 and i[pdd]!=None:
            new_cost[i[code_index]]["pdd_cost"]=round(float(i[pdd]),4)
        if i[jd]!=-1 and i[jd]!=None:
            new_cost[i[code_index]]["jd_cost"]=round(float(i[jd]),4)
        if i[tgc]!=-1 and i[tgc]!=None:
            new_cost[i[code_index]]["tgc_cost"]=round(float(i[tgc]),4)
    #操作mysql更新
    err_msg_list=[]
    for k,y in new_cost.items():
        try:
            c_obj=models.Finace_Cost.objects.filter(stylecode=k).first()
            if c_obj!=None:
                cur_obj=models.Finace_Cost.objects.filter(stylecode=c_obj.stylecode).update(**y)
                sql_log.info(f"操作人:{request.session['us_info'].User_name} 修改成本价 {k} {y}")
            else:
                cur_obj=models.Finace_Cost.objects.create(stylecode=k,**y)
                sql_log.info(f"操作人:{request.session['us_info'].User_name} 新增成本价 {k} {y}")

        except Exception as e:
            sql_log.error(f"{e}")
            err_msg_list.append(f"{k}更新成本价失败,原因{e}")
    if len(err_msg_list)==0:
        res.change(status=200,msg="所有成本价更新完成!",data={})
    else:
        res.change(status=98,msg=f"{','.join(err_msg_list)}",data={})
    return Response(res.get_dict)
