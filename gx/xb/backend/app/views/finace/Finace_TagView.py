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
#吊牌价序列化器
class FinaceTagSerializer(serializers.Serializer):
    shop = serializers.CharField(max_length=64)
    male_tag = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    female_tag = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    child_tag = serializers.DecimalField(max_digits=20, decimal_places=2,required=False)
    is_delete = serializers.IntegerField(default=0,required=False,write_only=True)  # 1=已删除 0=未删除

    #APIView重写create
    def create(self, validated_data):
        instance=models.finace_tag_price.objects.create(
            shop=validated_data['shop'],
            male_tag = validated_data['male_tag'],
            female_tag = validated_data['female_tag'],
            child_tag = validated_data['child_tag']
        )
        return instance

    #APIView重写update
    def update(self, instance, validated_data):
        if 'male_tag' in validated_data:
            instance.male_tag=validated_data['male_tag']
        if 'female_tag' in validated_data:
            instance.female_tag = validated_data['female_tag']
        if 'child_tag' in validated_data:
            instance.child_tag = validated_data['child_tag']
        instance.save()
        return instance

#成本价ViewSet
class FinaceTagViewSet(APIView):
    #get
    def get(self,request):
        res=MyResponse()
        try:
            obj=models.finace_tag_price.objects.all()
            obj_ser=FinaceTagSerializer(instance=obj,many=True)
            res.is_ok_count(obj_ser.data,len(obj_ser.data))
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98,msg=e,data={})
            return Response(res.get_dict)

    #post
    def post(self,request):
        res = MyResponse()  # 实例化myresponse
        myfuct=Myfunction(FinaceTagSerializer)#实例化myfunction
        add_res=myfuct.obj_add(rs_data=request.data)
        res.change(status=add_res['status'], msg=add_res['msg'], data=add_res['data'])
        return Response(res.get_dict)

class FinaceCostViewSetFilter(APIView):
    #get
    def get(self,request):
        res = MyResponse()
        if 'shop' not in request.data:
            res.need_parameter_err()
            return Response(res.get_dict)
        try:
            obj = models.finace_tag_price.objects.filter(shop=request.data['shop']).first()
            if obj is None:
                res.none_err()
                return Response(res.get_dict)
            obj_ser = FinaceTagSerializer(instance=obj)
            res.is_ok(obj_ser.data)
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98, msg=e, data={})
            return Response(res.get_dict)

    #put
    def put(self,request):
        res = MyResponse()
        if 'shop' not in request.data:
            res.need_parameter_err()
            return Response(res.get_dict)
        obj = models.finace_tag_price.objects.filter(shop=request.data['shop']).first()
        if obj is None:
            res.none_err()
            return Response(res.get_dict)
        obj_ser = FinaceTagSerializer(instance=obj, data=request.data)

        if not obj_ser.is_valid():
            res.check_err(obj_ser.errors)
            return Response(res.get_dict)
        else:
            obj_ser.save()
            res.is_ok(obj_ser.data)
            return Response(res.get_dict)

@api_view(['POST'])
def import_newTag(request):
    res = MyResponse()

    # 接收上传保存到本地
    file = request.FILES.get('file')
    template_str = f"{request.session['us_info'].User_name}-{get_now_date()}-"
    file_path=os.path.join(settings.MEDIA_ROOT, f'update_tag_files/{template_str}{file.name}')
    with open(file_path, "wb") as z:
        for i in file.chunks():
            z.write(i)

    # 读取上传文件覆盖数据库
    file_data=read_xlsx(path=file_path,header_line=0)
    #判断格式
    if "店铺" not in file_data[0] or "男装吊牌价" not in file_data[0] or "女装吊牌价" not in file_data[0] or "童装吊牌价" not in file_data[0]:
        res.change(status=98,msg="上传文件模板错误,请参考模板文件",data={})
        return Response(res.get_dict)
    shop_index,male,female,child_tag=file_data[0].index("店铺"),file_data[0].index("男装吊牌价"),\
                file_data[0].index("女装吊牌价"),file_data[0].index("童装吊牌价")

    new_cost={}
    for i in file_data[1:]:
        new_cost[i[shop_index]]={}
        if i[male]!=-1 and i[male]!=None:
            new_cost[i[shop_index]]["male_cost"]=round(float(i[male]),2)
        if i[female]!=-1 and i[female]!=None:
            new_cost[i[shop_index]]["female_cost"]=round(float(i[female]),2)
        if i[child_tag]!=-1 and i[child_tag]!=None:
            new_cost[i[shop_index]]["child_tag_cost"]=round(float(i[child_tag]),2)
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
