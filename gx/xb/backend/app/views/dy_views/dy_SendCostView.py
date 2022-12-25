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
class dySendCostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True,required=False)
    shop=serializers.CharField(max_length=64)
    now_date=serializers.DateField()
    stylecode=serializers.CharField(max_length=32)
    send_number=serializers.IntegerField(required=False,default=0)
    refund_number = serializers.IntegerField(required=False,default=0)
    today_price=serializers.DecimalField(max_digits=20,decimal_places=4,required=False)
    is_delete = serializers.IntegerField(default=0,required=False,write_only=True)  # 1=已删除 0=未删除

    # APIView重写create
    def create(self, validated_data):
        if 'send_number' in validated_data:
            send_number = validated_data['send_number']
        else:
            send_number=None
        if 'refund_number' in validated_data:
            refund_number = validated_data['refund_number']
        else:
            refund_number=None
        if 'today_price' in validated_data:
            today_price = validated_data['today_price']
        else:
            today_price=None
        instance = models.dy_sendcost.objects.create(
            shop=validated_data['shop'],
            now_date=validated_data['now_date'],
            stylecode=validated_data['stylecode'],
            send_number=send_number,
            refund_number=refund_number,
            today_price=today_price,
        )
        return instance

    # APIView重写update
    def update(self, instance, validated_data):
        # instance.shop = validated_data['stylecode']
        # instance.now_date = validated_data['now_date']
        # instance.stylecode = validated_data['stylecode']
        if 'send_number' in validated_data:
            instance.send_number = validated_data['send_number']
        if 'refund_number' in validated_data:
            instance.refund_number = validated_data['refund_number']
        if 'today_price' in validated_data:
            instance.today_price = validated_data['today_price']
        return instance

#ViewSet
class dySendCostViewSet(APIView):
    def get(self, request):
        res = MyResponse()
        request_data = request.GET.dict()
        # print(request_data)
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
            obj = models.dy_sendcost.objects.filter(**parameters).all().order_by('-now_date')
            obj_ser = dySendCostSerializer(instance=obj, many=True)
            res.is_ok(obj_ser.data)
            return Response(res.get_dict)
        except Exception as e:
            res.change(status=98, msg=e, data={})
            return Response(res.get_dict)

