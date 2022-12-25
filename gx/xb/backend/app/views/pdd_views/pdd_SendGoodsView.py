from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt,csrf_protect  #csrf_exempt局部禁用  csrf_protect启用/
import json

from app import models
from util.mycls import MyResponse,Myfunction
#序列化器
class pddSendGoodsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    shop = serializers.CharField(max_length=64)
    now_date = serializers.DateField()
    order_number = serializers.IntegerField()
    is_delete = serializers.IntegerField(default=0, required=False, write_only=True)  # 1=已删除 0=未删除


#ViewSet
class pddSendGoodsViewSet(APIView):
    def get(self,request):
        res = MyResponse()
        request_data = request.GET.dict()
        try:
            parameters = {}
            if 'shop' in request_data and request_data['shop'] != None and request_data['shop']!="":
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
            obj = models.pdd_sendgoods.objects.filter(**parameters).all().order_by('-now_date')
            obj_ser = pddSendGoodsSerializer(instance=obj, many=True)
            res.is_ok(obj_ser.data)
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98, msg=e, data={})
            return Response(res.get_dict)
