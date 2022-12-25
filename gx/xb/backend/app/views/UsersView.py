import json
import requests.utils
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
from rest_framework.decorators import api_view
from django_redis import get_redis_connection
import smtplib
from urllib.parse import quote_plus
from uuid import uuid4

from app import models
from util.mycls import MyResponse,Myfunction
from conf.exts import *
#用户序列化器
class UsersSerializer(serializers.Serializer):
    User_id = serializers.IntegerField(read_only=True,required=False)
    User_name = serializers.CharField(max_length=8)
    User_email = serializers.CharField(max_length=30)
    User_password = serializers.CharField(max_length=16)
    User_face = serializers.ImageField(default='face_img/default_face.JPG') # 图片重写存储方法 重命名写入
    User_erp_cookies=serializers.CharField(max_length=500,required=False)
    is_delete = serializers.IntegerField(default=0, required=False, write_only=True)  # 1=已删除 0=未删除

    def create(self, validated_data):
        parameters={}
        if 'User_name' in validated_data:
            parameters['User_name']=validated_data['User_name']
        if 'User_email' in validated_data:
            parameters['User_email']=validated_data['User_email']
        if 'User_password' in validated_data:
            parameters['User_password']=make_password(validated_data['User_password'])
        if 'User_face' in validated_data:
            parameters['User_face']=validated_data['User_face']
        instance=models.Users.objects.create(**parameters)
        return instance

    def update(self, instance, validated_data):
        if 'User_password' in validated_data:
            instance.User_password = make_password(validated_data['User_password'])
        if 'User_face' in validated_data:
            instance.User_face = validated_data['User_face']
            print(f"头像---{validated_data['User_face']}")
        instance.save()
        return instance

#用户ViewSet
class UsersViewSet(APIView):
    #创建新用户
    def post(self,request):
        res=MyResponse()
        request_data = request.data
        if 'User_name' not in request_data or 'User_email' not in request_data or 'User_password' not in request_data or 'vcode' not in request_data:
            res.need_parameter_err()
            return Response(res.get_dict)

        check_obj=models.Users.objects.filter(Q(User_email=request_data['User_email'])|Q(User_name=request_data['User_name'])).first()
        if check_obj!=None:
            if check_obj.User_email==request_data['User_email']:
                msg = "此邮箱已经注册"
            elif check_obj.User_name==request_data['User_name']:
                msg = "此用户已经拥有一个账号"
            else:
                msg = "注册失败,请联系管理员"
            res.change(status=98, msg=msg, data={})
            return Response(res.get_dict)

        #验证码验证
        dj_rds = get_redis_connection('verify_code')
        vcode = dj_rds.get(f"vcode-{request_data['User_email']}")
        if vcode is None:
            msg = "验证码已失效或者验证码未发送"
            res.change(status=98,msg=msg,data={})
            return Response(res.get_dict)
        elif vcode.decode() != request_data['vcode']:
            msg = "验证码错误"
            res.change(status=98, msg=msg, data={})
            return Response(res.get_dict)
        myfuct=Myfunction(UsersSerializer)
        add_res=myfuct.obj_add(rs_data=request_data)
        if add_res['status']==200:
            res.change(status=add_res['status'],msg="注册"+add_res['msg'],data=add_res['data'])
        else:
            res.change(status=98,msg=add_res['msg'],data={})
        return Response(res.get_dict)

class UsersViewSetFilter(APIView):
    pass

#登录
@api_view(['POST'])
def us_login(request):
    res=MyResponse()
    dj_rs = Response()
    request_data=request.data
    #必要参数 邮箱和密码
    if "User_email" not in request_data or "User_password" not in request_data:
        res.need_parameter_err()
        return Response(res.get_dict)

    us_obj=models.Users.objects.filter(User_email=request_data['User_email']).first()
    #1.查看邮箱是否存在
    if us_obj is None:
        res.change(status=98,msg="此邮箱账号不存在",data={})
        return Response(res.get_dict)
    #2.验证码密码是否正确
    if check_password(request_data['User_password'],us_obj.User_password):
        # 3.登录成功
        res.change(status=200,msg="登录成功",data={'User_name':us_obj.User_name,'User_email':us_obj.User_email,'User_face':us_obj.User_face.url,'User_erp_cookies':us_obj.User_erp_cookies})
        #设置session
        # 1.登录之前检查此客户端是否 已经存在session_key 存在则删掉 不存在则创建
        if request.session.exists(request.session.session_key):
            request.session.flush()

        request.session['us_info']=us_obj
        #设置Response data
        dj_rs.data=res.get_dict
    else:
        res.change(status=98,msg="密码验证错误",data={})
    return dj_rs



#发送邮件
@api_view(['POST'])
def create_vcode(request):
    res=MyResponse()
    request_data = request.data
    #随机生成6位数验证码
    vcode=generate_code()

    # 验证码临时存入redis session
    dj_rds=get_redis_connection('verify_code')
    dj_rds.set(f"vcode-{request_data['email']}",vcode,300) #300秒验证码有效期

    #发送邮件
    rs=send_email(addressee_email=request_data['email'],vcode=vcode)
    if rs:
        res.change(status=200,msg="邮件发送成功,15s内只可发送一次邮件!",data={})
    else:
        res.change(status=98,msg="邮件发送失败,请重试或联系管理员！",data={})
    return Response(res.get_dict)

#查看邮箱是否存在
@api_view(['GET'])
def check_email(request):
    res=MyResponse()
    #接收cookies并验证
    obj=request.session.get("us_info")
    # print(obj)
    request_data=request.GET.dict()
    obj=models.Users.objects.filter(User_email=request_data['email']).first()
    if obj is None:
        res.change(status=200,msg="邮箱可以注册",data={})
    else:
        res.change(status=98,msg="邮箱已经被注册",data={})
    return Response(res.get_dict)

#验证session接口
@api_view(['GET','POST'])
def check_session(request):
    res=MyResponse()
    if request.method=="POST":
        us_obj=request.session.get('us_info')
        res.is_ok(data={'User_name':us_obj.User_name,'User_email':us_obj.User_email,'User_face':us_obj.User_face.url,'User_erp_cookies':us_obj.User_erp_cookies})
    else:
        res.is_ok(data={})
    return Response(res.get_dict)