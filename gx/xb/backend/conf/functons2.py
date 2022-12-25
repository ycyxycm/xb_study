import ctypes
import inspect

from django.db.models import Sum,F

from util.dy_count_cls import dySales,dySurvey
from app import models
from itertools import zip_longest

SHOP_MATCHING_DICT={'PDD童装-史努比炫派专卖店': 'PDD童装史努比炫派专卖店', 'PDD女装-雅希恩旗舰店': 'PDD女装雅希恩旗舰店',
                    'PDD童装-婴麦奇旗舰店': 'PDD童装婴麦奇旗舰店', 'PDD女装-IM DAVID小布家': 'PDD女装IMDAVID小布家',
                    'PDD童装-拉夏贝尔格仕洛': 'PDD童装拉夏贝尔格仕洛', 'PDD童装-布朗熊增春': 'PDD童装布朗熊增春',
                    'PDD女装-叮当制造官方旗舰店': 'PDD女装叮当制造官方旗舰店', 'PDD女装-高梵杰伊斯店': 'PDD女装高梵杰伊斯店',
                    'PDD童装-高梵麦威伦店': 'PDD童装高梵麦威伦店', 'PDD童装-布朗熊炫派专卖店': 'PDD童装布朗熊炫派专卖店',
                    'PDD女装-IMDAVID禾季纯专卖店': 'PDD女装IMDAVID禾季纯专卖店', 'PDD男装-高梵锐迈鑫店': 'PDD男装高梵锐迈鑫店',
                    'PDD男装-ESSECITY旗舰店': 'PDD男装ESSECITY旗舰店', 'PDD男装-IM DAVID优昌源专卖店': 'PDD男装IMDAVID优昌源专卖店',
                    'PDD女装-雪中飞飘思芬专卖店': 'PDD女装雪中飞飘思芬专卖店', 'PDD男装-高梵禾季纯店': 'PDD男装高梵禾季纯店',
                    'PDD男装-雪中飞聚沙成塔专卖店': 'PDD男装雪中飞聚沙成塔专卖店', 'PDD女装-雪中飞阅香时代专卖店': 'PDD女装雪中飞阅香时代专卖店',
                    'PDD童装-布朗熊较真专卖店': 'PDD童装布朗熊较真专卖店', 'PDD童装-雪中飞禾季纯专卖店': 'PDD童装雪中飞禾季纯专卖店',
                    'PDD童装-田芽旗舰店': 'PDD童装田芽旗舰店', 'PDD女装-黑白町官方旗舰店': 'PDD女装黑白町官方旗舰店',
                    'PDD女装-久做范儿女装旗舰店': 'PDD女装久做范儿女装旗舰店', 'PDD女装-语霖旗舰店': 'PDD女装语霖旗舰店',
                    'PDD女装-RESHAKE炫派专卖店': 'PDD女装RESHAKE炫派专卖店', 'PDD女装-IM DAVID较真专卖店': 'PDD女装IMDAVID较真专卖店',
                    'PDD女装-IM DAVID喵思范专卖店': 'PDD女装IMDAVID喵思范专卖店', 'PDD男装-IM DAVID聚沙成塔专卖店': 'PDD男装IMDAVID聚沙成塔专卖店',
                    'PDD男装-布衣不二旗舰店': 'PDD男装布衣不二旗舰店', 'PDD男装-JEANSWEST真维斯休闲装旗舰店': 'PDD男装JEANSWEST真维斯休闲装旗舰店',
                    'PDD女装-真维斯较真专卖店': 'PDD女装真维斯较真专卖店', 'PDD女装-真维斯阅香时代专卖店': 'PDD女装真维斯阅香时代专卖店',
                    'PDD童装-布朗熊阅香时代': 'PDD童装布朗熊阅香时代', 'PDD女装-玩未锐越专卖店': 'PDD女装玩未锐越专卖店',
                    'PDD女装-蓝卓恩官方旗舰店': 'PDD女装蓝卓恩官方旗舰店', 'PDD女装-莫妮希旗舰店': 'PDD女装莫妮希旗舰店'}

def dy_count_function(index,res_list):
    ds=dySales(res_list[index])
    ds.new_date()
    res_list[index]=ds.get_dict

def dy_suery_count_function(shop_name,start_date,end_date,all_dict):
    ds=dySurvey(shop=shop_name,start_date=start_date,end_date=end_date)
    all_dict.append(ds.get_dict)

#拼多多替换掉多维度导出数据中的部分字段值
def change_val(par_dict,date):
    reversal=dict(zip(SHOP_MATCHING_DICT.values(),SHOP_MATCHING_DICT.keys()))
    cur_dict=par_dict
    cur_shop=reversal[cur_dict['shop']]
    cur_sales_obj = models.pdd_sales.objects.filter(shop=cur_shop, now_date=date).first()
    if "付款订单金额" in cur_dict:
        cur_dict['付款订单金额']=0 if cur_sales_obj is None else float(cur_sales_obj.deal_price)
    if "销售成本" in cur_dict:
        cur_cost_count = models.pdd_sendcost.objects.filter(shop=cur_shop, now_date=date).aggregate(
            cost_count=Sum(F("send_number") * F("today_price")))['cost_count']
        cur_dict['销售成本']=0 if cur_cost_count is None else float(cur_cost_count)
    if "发货前退款额" in cur_dict and "发货后退款额" in cur_dict:
        #发货前退款额=退款-发货后退款额
        cur_refund=0 if cur_sales_obj is None else float(cur_sales_obj.refund_price)#退款
        cur_dict['发货前退款额']=cur_refund-cur_dict['发货后退款额']
    if 'shop' in cur_dict:
        cur_dict['shop']=reversal[cur_dict['shop']]
    return cur_dict

def _async_raise( tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:

        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread( thread):
    try:
        _async_raise(thread.ident, SystemExit)
    except Exception:
        pass

#反转字典
def invert_dict(d):
    return dict(zip(d.itervalues(), d.iterkeys()))





