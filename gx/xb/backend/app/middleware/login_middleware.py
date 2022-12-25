import json

from django.shortcuts import HttpResponse,render,redirect,HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
import re

from util.mycls import MyResponse
from conf.exts import get_request_ip

class login_midd(MiddlewareMixin):
    def process_request(self, request):
        white_list=['/login','/us/register/checkemail','/us/register/cemail']#不带session可以访问的地址
        post_whiter_list=['/user']
        cur_path=request.path
        if cur_path in white_list:
            print("白名单路由,放行")
            return None
        elif cur_path in post_whiter_list and request.method=="POST":
            print("白名单路由,放行")
            return None
        else:
            user = request.session.get('us_info')
            if request.session.exists(request.session.session_key) and user != None:
                return None
            else:
                print("未检测到session,请先登陆再进行操作")
                res = MyResponse()
                res.session_err()
                return HttpResponse(json.dumps(res.get_dict))

