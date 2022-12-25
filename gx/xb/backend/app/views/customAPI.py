from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt,csrf_protect  #csrf_exempt局部禁用  csrf_protect启用/
import json
from rest_framework.decorators import api_view

from app import models
from util.mycls import MyResponse,Myfunction


# #抖店 成交退款金额 运费险数据API
# @api_view(['GET'])#{"shop_ck_list":[{"shop_name":"张三店",'cookies':'1212312321','date':'2022-10-01'}]}
# def get_all_dydata(request):
#     res = MyResponse()
#     if 'shop_ck_list' not in request.data:
#         res.need_parameter_err()
#         return Response(res.get_dict)
#     date_re_list=[]
#     for i in json.loads(request.data['shop_ck_list']):
#         if 'shop_name' not in i or 'cookies' not in i or 'date' not in i:
#             res.need_parameter_err()
#             return Response(res.get_dict)
#         data_dict = {}
#         mycls=dy_doudian(cookies=i['cookies'])
#         cjtk=mycls.get_cjtk(i['date'])
#         yfx=mycls.get_yfx(i['date'])
#         if cjtk['status']!=100 or yfx['status']!=100:
#             res.change(status=-1,msg=cjtk['msg']+"/"+yfx['msg'],data={})
#             return Response(res.get_dict)
#         data_dict['shop_name']=i['shop_name']
#         data_dict['cj_price']=cjtk['data']['cj_price']
#         data_dict['tk_price']=cjtk['data']['tk_price']
#         data_dict['yfx']=yfx['data']
#         data_dict['date']=i['date']
#
#         date_re_list.append(data_dict)
#     res.is_ok(data=date_re_list)
#     return Response(res.get_dict)
#
#
