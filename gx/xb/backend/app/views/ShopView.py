from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt,csrf_protect  #csrf_exempt局部禁用  csrf_protect启用/
import json

from app import models
from util.mycls import MyResponse,Myfunction
#店铺序列化器
class ShopSerializer(serializers.Serializer):
    Shop_id = serializers.IntegerField(read_only=True,required=False)
    Shop_name = serializers.CharField(max_length=64)
    Shop_pallet = serializers.CharField(max_length=12)
    is_delete = serializers.IntegerField(default=0,required=False,write_only=True)  # 1=已删除 0=未删除

    #APIView重写create
    def create(self, validated_data):
        instance=models.Shop.objects.create(
            Shop_name=validated_data['Shop_name'],
            Shop_pallet=validated_data['Shop_pallet']
        )
        return instance

    # APIView重写update
    def update(self, instance, validated_data):
        instance.Shop_name=validated_data['Shop_name']
        instance.Shop_pallet=validated_data['Shop_pallet']
        instance.save()
        return instance

#店铺ViewSet
class ShopViewSet(APIView):
    #get
    def get(self,request):
        res=MyResponse()
        obj=models.Shop.objects.all()
        obj_ser=ShopSerializer(instance=obj,many=True)
        res.is_ok(obj_ser.data)
        res2=res.get_dict
        res2['count']=len(res.data)
        return Response(res2)
    #post
    def post(self,request):
        res = MyResponse()#实例化myresponse
        myfuct=Myfunction(ShopSerializer)
        add_res=myfuct.obj_add(request.data)
        res.change(status=add_res['status'],msg=add_res['msg'],data=add_res['data'])
        return Response(res.get_dict)

#filter
class ShopViewSetFilter(APIView):
    # get
    def get(self, request,id):
        res = MyResponse()
        try:
            obj = models.Shop.objects.filter(Shop_id=id).first()
            if obj is None:
                res.none_err()
                return Response(res.get_dict)
            obj_ser = ShopSerializer(instance=obj)
            res.is_ok(obj_ser.data)
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98,msg=e,data={})
            return Response(res.get_dict)

    #修改
    def put(self,request,id):
        res = MyResponse()
        obj = models.Shop.objects.filter(Shop_id=id).first()
        if obj is None:
            res.none_err()
            return Response(res.get_dict)
        obj_ser = ShopSerializer(instance=obj, data=request.data)

        if not obj_ser.is_valid():
            res.check_err(obj_ser.errors)
            return Response(res.get_dict)
        else:
            obj_ser.save()
            res.is_ok(obj_ser.data)
            return Response(res.get_dict)

    #删除指定id
    def delete(self,request,id):
        res = MyResponse()
        try:
            obj=models.Shop.objects.get(Shop_id=id)
            shop_name=obj.Shop_name
            obj.delete()
            res.is_ok("已删除:"+str(shop_name))
            return Response(res.get_dict)
        except Exception as e:
            return Response(res.get_dict)


#批量添加店铺
@csrf_exempt
def many_shop_add(request):
    return_list=[]
    data_list=json.loads(request.body)
    for i in data_list:
        try:
            myfuct=Myfunction(ShopSerializer)
            current_add_res=myfuct.obj_add(i)
            status,msg=current_add_res['status'],current_add_res['msg']
        except Exception as e:
            status, msg = 98,e
        return_list.append({'Shop_name': i['Shop_name'], 'status': status, 'msg': msg})
    return JsonResponse({'data':return_list})
