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
class CookiesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    Shop = serializers.CharField(max_length=64)
    Shop_pallet = serializers.CharField(max_length=12)
    cookies = serializers.CharField(max_length=10000)
    update_time = serializers.DateTimeField()

    #APIView重写create
    def create(self, validated_data):
        instance=models.cookies_all.objects.create(
            Shop=validated_data['Shop'],
            Shop_pallet=validated_data['Shop_pallet'],
            cookies=validated_data['cookies'],
            update_time=validated_data['update_time'],
        )
        return instance

    # APIView重写update
    def update(self, instance, validated_data):
        # instance.Shop=validated_data['Shop']
        # instance.Shop_pallet=validated_data['Shop_pallet']
        instance.cookies = validated_data['cookies']
        instance.update_time = validated_data['update_time']
        instance.save()
        return instance

#店铺ViewSet
class CookiesViewSet(APIView):
    #get
    def get(self,request):
        res=MyResponse()
        obj=models.cookies_all.objects.all()
        obj_ser=CookiesSerializer(instance=obj,many=True)
        res.is_ok(obj_ser.data)
        res2=res.get_dict
        res2['count']=len(res.data)
        return Response(res2)
