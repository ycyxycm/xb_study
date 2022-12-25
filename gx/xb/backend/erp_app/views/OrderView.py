from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time
import logging

from util.grabData_cls import erp_stock
from util.mycls import MyResponse
from erp_app import models
@api_view(['POST'])
def get_orders(request):
    white_list=['女装程序换福袋','男装程序换福袋','测试订单','红包卡单','福袋缺货']#,'商品资料不存在'
    res=MyResponse()
    request_data=request.data
    #检测异常
    if 'abn' not in request_data:
        res.need_parameter_err()
        return Response(res.get_dict)
    if request_data['abn'] not in white_list:
        res.change(status=98,msg="当前异常类型不支持福袋操作",data={})
        return Response(res.get_dict)

    usobj=request.session.get('us_info')
    es=erp_stock(usobj.User_erp_cookies)
    try:
        data_list=es.get_order_all(abn_name=request_data['abn'])
        res.is_ok(data=data_list)
        return Response(res.get_dict)
    except Exception as e:
        res.change(status=98,msg=f"爬取数据出现问题--{e}",data={})
        return Response(res.get_dict)

#匹配可用库存 变为成品装
@api_view(['POST'])
def matching_stock(request):
    res=MyResponse()
    usobj = request.session.get('us_info')
    es=erp_stock(usobj.User_erp_cookies)
    request_data=request.data
    oid_info_list=request_data
    for i in oid_info_list:#循环订单
        cur_items=i['items']#当前订单所有 商品
        cur_can_stock_dict=es.get_can_stock(i['o_id'])
        cur_matching_dict=cur_can_stock_dict['data']
        if cur_can_stock_dict['status']!=200:
            res.change(status=98,msg=cur_can_stock_dict['msg'],data={})
            return Response(res.get_dict)
        for j in cur_items:#循环订单内的商品
            if j['sku_id'] in cur_matching_dict:
                j['can_stock']=cur_matching_dict[j['sku_id']]
            else:
                j['can_stock']="err"
        time.sleep(0.5)
    res.change(status=200,msg='可用库存匹配完成!',data=oid_info_list)
    return Response(res.get_dict)

#匹配福袋 变为成品装
@api_view(['POST'])
def matching_fd(request):
    res=MyResponse()
    matching_err_oid_list=[]#匹配失败的内部订单号
    request_data=request.data
    if 'data' not in request_data or 'stock_type' not in request_data or 'type_sex' not in request_data:
        res.need_parameter_err()
        return Response(res.get_dict)
    oid_info_list=request_data['data']
    for i in oid_info_list:#循环订单
        cur_items=i['items']
        cur_use_code=[]#当前订单已经使用的编码
        parameters = {}#查询参数
        for j in cur_items:#循环订单内的商品
            #只替换福袋
            if "福袋" in j['sku_id'] and request_data['stock_type']==False:
                parameters['commodity_code__startswith'] = j['sku_id'].replace('福袋', '')#查询参数
                cur_newskuid_list=[]
                for z in range(j['qty']):
                    if request_data['type_sex']:#True则匹配女装仓库
                        info = models.female_stock.objects.filter(**parameters).exclude(commodity_code__in=cur_use_code).order_by('?')[:1].first()#单个福袋匹配的成品装.first()
                    else:#False则匹配男装仓库
                        info = models.male_stock.objects.filter(**parameters).exclude(commodity_code__in=cur_use_code).order_by('?')[:1].first()#单个福袋匹配的成品装.first()
                    if info == None:
                        cur_newskuid_list.append("福袋匹配失败")
                        matching_err_oid_list.append(i['o_id'])
                    else:
                        cur_newskuid_list.append(info.commodity_code)
                        cur_use_code.append(info.commodity_code)
                #循环完了之后将cur_newskuid_list用,拼接为字符串 赋值给j['newsku_id']
                j['newsku_id']=','.join(cur_newskuid_list)
            elif 'can_stock' in j and request_data['stock_type']==True:
                if j['can_stock']=="err":
                    pass
                elif j['can_stock']<=0:
                    parameters['commodity_code__startswith'] = "-".join(j['sku_id'].split("-")[:3])# 查询参数
                    cur_newskuid_list = []
                    for z in range(j['qty']):
                        if request_data['type_sex']:  # True则匹配女装仓库
                            info = models.female_stock.objects.filter(**parameters).exclude(
                                commodity_code__in=cur_use_code).order_by('?')[:1].first()  # 单个福袋匹配的成品装.first()
                        else:  # False则匹配男装仓库
                            info = models.male_stock.objects.filter(**parameters).exclude(
                                commodity_code__in=cur_use_code).order_by('?')[:1].first()  # 单个福袋匹配的成品装.first()
                        if info == None:
                            cur_newskuid_list.append("福袋匹配失败")
                            matching_err_oid_list.append(i['o_id'])
                        else:
                            cur_newskuid_list.append(info.commodity_code)
                            cur_use_code.append(info.commodity_code)
                    # 循环完了之后将cur_newskuid_list用,拼接为字符串 赋值给j['newsku_id']
                    j['newsku_id'] = ','.join(cur_newskuid_list)
    matching_err_oid_list=[str(i) for i in matching_err_oid_list]
    if len(matching_err_oid_list)<=0:
        msg="福袋全部匹配完成!"
    else:
        cur_str_msg='\n'.join(matching_err_oid_list)
        msg=f"福袋部分匹配失败:\n{cur_str_msg}"
    res.change(status=200,msg=msg,data=oid_info_list)
    return Response(res.get_dict)

#修改操作
@api_view(['POST'])
def change_fd(request):
    fd_log=logging.getLogger('fd_log')
    logger_info_msg_list=[]#操作记录列表
    used_code=[]#用过的商品编码 替换完成后需要删除
    black_list=['福袋匹配失败']
    res=MyResponse()
    usobj = request.session.get('us_info')
    request_data=request.data#请求过来的数据为单个内部订单号的 json数据
    #1.获取内部订单号
    cur_oid_info=request_data['o_id']
    #2.获取当前订单号中的 所有商品id
    cur_shop_all=request_data['items']
    #3.遍历当前订单中的 所有商品 如果当前json中有new_sku字段则进行替换
    dataCount_list=[]
    CALLBACKPARAM = {
        "Method": "ChangeBatchItem",
        "Args": [int(cur_oid_info),{"items":dataCount_list}],
        "CallControl": "{page}"
    }
    try:
        for i in cur_shop_all:
            if "newsku_id" not in i:#有新的sku则进行替换 无则跳过
                pass
            elif i['newsku_id'] in black_list:
                pass
            else:#newsku_id存在的话 则是需要替换的
                #A.先删除旧的sku
                del_dict={
                    "sku_id": i['newsku_id'],
                    "qty": i['qty'],
                    "price": i['price'],
                    "amount": i['amount'],
                    "is_gift": False,
                    "oi_id": i['oi_id'],
                    "is_del": True,
                    "il_id": None,
                    "sku_type": "normal",
                    "is_new": False
                }
                dataCount_list.append(del_dict)
                #B.用,分隔 newsku_id 新增新的sku
                cur_newskuid_list=i['newsku_id'].split(',')
                if len(cur_newskuid_list)!=i['qty']:
                    res.change(status=98,msg=i['oi_id']+"替换之后的数量和之前数量不一致,替换失败",data={})
                    return Response(res.get_dict)
                    # continue
                else:
                    logger_info_msg_list.append(f"操作人:{usobj.User_name} 内部订单id:{cur_oid_info}   {i['sku_id']}   >>>>>>>>>>>   {i['newsku_id']}")
                    for z in cur_newskuid_list:
                        cur_sondict = {
                            "sku_id":z,
                            "qty": 1,
                            "price": round(i['price']/i['qty'],2),
                            "amount": round(1*i['price'],2),
                            "is_gift": False,
                            "oi_id": 0,
                            "is_del": False,
                            "is_new": True
                        }
                        dataCount_list.append(cur_sondict)
                        used_code.append(z)
    except Exception as e:
        res.change(status=98,msg="错误原因"+str(e),data={})
        fd_log.error(f"{cur_oid_info} 福袋替换失败 原因:{str(e)}")
        return Response(res.get_dict)
    #删除已使用过的商品编码
    used_obj_all=models.male_stock.objects.filter(commodity_code__in=used_code).all()
    if used_obj_all!=None:
        for g in used_obj_all:
            if g.number<=1:
                # print(f"{g.commodity_code}删除")
                g.delete()
            else:
                g.number-=1
                g.save()
                # print(f"{g.commodity_code}数量减一")
    #4.成功则调用聚水潭替换福袋操作
    es=erp_stock(usobj.User_erp_cookies)
    change_rs=es.change_code(CALLBACKPARAM=CALLBACKPARAM)
    if change_rs['IsSuccess']:
        status =200
    else:
        status=98
    if change_rs['ExceptionMessage']==None:
        msg='\n'.join(logger_info_msg_list)
        [fd_log.info(i) for i in logger_info_msg_list]
    else:
        msg=change_rs['ExceptionMessage']

    res.change(status=status,msg=msg,data={})
    return Response(res.get_dict)

