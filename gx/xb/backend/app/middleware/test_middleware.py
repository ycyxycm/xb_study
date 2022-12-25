from django.shortcuts import HttpResponse,render,redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
import re,logging

from conf.exts import get_request_ip,print_cyan

lg=logging.getLogger('api_log')
#不拦截 纯打印
class testMiddleware(MiddlewareMixin):
    def process_request(self,request):
        white_list = ['/login','/us/register/checkemail','/us/register/cemail']  # 不带session可以访问的地址
        post_whiter_list = ['/user']
        cur_path=request.path
        cur_method=request.method
        ip = get_request_ip(request=request)
        if cur_path in white_list:
            lg.info(f"[{ip}] 未登陆操作 接口Path: {cur_path} 请求方式: {cur_method}")
        elif cur_path in post_whiter_list and request.method=="POST":
        # elif cur_path in log_path and request.method=="POST":
            lg.info(f"[{ip}] 未登陆操作 接口Path: {cur_path} 请求方式: {cur_method}")
        else:
            user = request.session.get('us_info')
            lg.info(f"[{ip}] 调用人: {user.User_name}  接口Path: {cur_path} 请求方式: {cur_method}")
        return None