import xlrd

from dy_get_data.dy_erp_data import erp_info
from util.mysqlConfig import mysql_config
from exts import *

#1.筛选
def filter_data(data_counts):
    new_data_counts=[]
    for i in data_counts:# 筛选
        # 店铺带 ' 的替换为空
        if i['店铺'] is None:
            continue
        else:
            i['店铺'] = i['店铺'].replace("'", "")

        # 如果款式编码包含辅料的话则 取商品编码值
        if i["款式编码"] is None:
            pass
        elif "辅料" in i["款式编码"]:
            i["款式编码"]=i["商品编码"]

        # 线上商品名：无须，无需，差价。带这几个关键字的就删掉
        if i['线上商品名'] is None:
            pass
        elif "无需" in i['线上商品名'] or "无须" in i['线上商品名'] or "差价" in i['线上商品名']:
            continue

        # 标记多标签：补单关键字全部删掉
        if i["标记多标签"] is None:
            pass
        elif '补单' in i["标记多标签"]:
            if '未设定' in i['发货仓']:  # 补单没发货
                continue
            else:  # 补单发货
                i['款式编码'] = "补单发货编码"

        # 款式编码：烫画，包裹卡，白坯，白胚两个字替换掉，辅料用前面的商品编码填充过去
        if i['款式编码'] is None:
            pass
        elif "烫画" in i['款式编码'] or "包裹卡" in i['款式编码']:
            continue
        elif "白坯" in i['款式编码'] or "白胚" in i['款式编码']:
            i['款式编码']=i['款式编码'].replace("白坯","").replace("白胚","")
        new_data_counts.append(i)
    return new_data_counts

#1.售后主题分析筛选
def sh_filter_data(data_counts):
    new_data_counts = []
    for i in data_counts:  # 筛选
        # 店铺带 ' 的替换为空
        if i['店铺'] is None:# or i['款式编码'] is None
            continue
        else:
            i['店铺'] = i['店铺'].replace("'", "")

        # 款式编码：烫画，包裹卡，白坯，白胚两个字替换掉，辅料用前面的商品编码填充过去
        if i['款式编码'] is None:
            pass
        # elif "烫画" in i['款式编码'] or "包裹卡" in i['款式编码']:
        #     continue
        elif "白坯" in i['款式编码'] or "白胚" in i['款式编码']:
            i['款式编码'] = i['款式编码'].replace("白坯", "").replace("白胚", "")
        new_data_counts.append(i)
    return new_data_counts

#2.计算各个店铺订单数 去重原始线上订单号
def count_orders(data_counts):
    count_dict={}
    for i in data_counts:
        if i['店铺'] not in count_dict:
            count_dict[i['店铺']]=[]
        count_dict[i['店铺']].append(i['原始线上订单号'])
        count_dict[i['店铺']]=list(set(count_dict[i['店铺']]))
    for k,y in count_dict.items():
        count_dict[k]=len(y)
    return count_dict

#3.统计各个店铺各个款式的发货数量
def count_sendshop(data_counts):
    count_dict={}#{"店铺":{"款式名":""数量},"店铺":{"款式名":""数量},"店铺":{"款式名":""数量}}
    for i in data_counts:
        if i['店铺'] not in count_dict:
            count_dict[i['店铺']] = {}
        if i['款式编码'] not in count_dict[i['店铺']]:
            count_dict[i['店铺']][i['款式编码']]=0
        if i['销售数量']!=None:
            count_dict[i['店铺']][i['款式编码']]+=i['销售数量']
    return count_dict

#3.统计各个店铺各个款式的退货数量
def count_refundshop(data_counts):
    count_dict = {}  # {"店铺":{"款式名":""数量},"店铺":{"款式名":""数量},"店铺":{"款式名":""数量}}
    for i in data_counts:
        if i['店铺'] not in count_dict:
            count_dict[i['店铺']] = {}
        if i['款式编码'] not in count_dict[i['店铺']]:
            count_dict[i['店铺']][i['款式编码']] = 0
        if i['退货数量'] != None:
            count_dict[i['店铺']][i['款式编码']] += i['实退数量']
    return count_dict

#4.通过款式编码查询当天成本价(抖音)
def get_today_cost(stylecode):
    mycls=mysql_config()
    sql=f'select * from finace_cost where stylecode="{stylecode}"'
    res=mycls.sql_fetch(sql)
    if len(res)==0:
        raise ValueError(f"成本价查询失败,建议将send_cost表今日数据删除重新跑--{stylecode}")
    else:
        return res[0][1]

#抓取筛选售后数据
def dy_sh_main(cookies,date):
    mycls = erp_info(cookies=cookies)
    refund_data_counts = mycls.get_dy_shztfx_table(date=date)
    print(f"售后主题分析列表长度:{len(refund_data_counts)}")
    refund_data_counts = sh_filter_data(data_counts=refund_data_counts)
    print(f"售后主题分析筛选后列表长度:{len(refund_data_counts)}")
    print("\n")

    # 3.统计各个店铺各个款式的退货数量
    print("统计各个店铺各个款式的退货数量")
    refund_shop_dict = count_refundshop(data_counts=refund_data_counts)
    print(refund_shop_dict)
    print("\n")
    return refund_shop_dict


def dy_zt_main(cookies,date):
    mycls = erp_info(cookies=cookies)

    data_counts = mycls.get_dy_ztxsfx_table(date=date)
    print(f"开始对主题分析表进行筛选  筛选前 {len(data_counts)} 条")
    data_counts = filter_data(data_counts)
    print(f"主题销售分析 筛选后的数据计 {len(data_counts)} 条")
    print("\n")

    # 2.计算各个店铺订单数 去重原始线上订单号
    print("计算各个店铺订单数 去重原始线上订单号")
    orders_count_dict = count_orders(data_counts=data_counts)
    print(orders_count_dict)
    print("\n")

    # 3.统计各个店铺各个款式的发货数量
    print("统计各个店铺各个款式的发货数量")
    send_shop_dict = count_sendshop(data_counts=data_counts)
    print(send_shop_dict)
    print("\n")

    # 4.获取多维度数据
    dwd_orders_dict={}
    print("统计各个店铺多维度  发货后退款成本")
    dwd_dict=mycls.get_sf_cost(date=date)
    print(dwd_dict)

    # 5.将多维度数据与订单数据字典合并 {shop:店铺名,send_order:订单数量,sf_cost:发货后退款成本}
    for k,y in dwd_dict.items():
        if k not in dwd_orders_dict:
            dwd_orders_dict[k] = {'dwd':0,'orders':0}
        dwd_orders_dict[k]['dwd']=y
    for k1, y1 in orders_count_dict.items():
        if k1 not in dwd_orders_dict:
            dwd_orders_dict[k1] = {'dwd':0,'orders':0}
        dwd_orders_dict[k1]['orders']=y1




    #合并完成的字典打印
    print(dwd_orders_dict)
    return {'dwd_orders_dict':dwd_orders_dict,'send_shop_dict':send_shop_dict}


def dy_sql_main(date,erp_cookies):
    refund_shop_dict = dy_sh_main(cookies=erp_cookies, date=date)
    zt_dict = dy_zt_main(cookies=erp_cookies, date=date)
    orders_count_dict=zt_dict['dwd_orders_dict']
    send_shop_dict=zt_dict['send_shop_dict']

    print("#######################开始写入抖音订单数据#################################")
    for k, y in orders_count_dict.items():
        sql_cls = mysql_config()
        sql = f"insert into dy_sendgoods values(null,'{date}',{y['orders']},0,'{k}',{y['dwd']})"
        rs = sql_cls.sql_commit(sql)
        if rs:
            print(f"店铺{k},日期{date},写入数据库成功")
        else:
            print(f"店铺{k},日期{date},SQL持久化出错")
        sql_cls.close_db()
    print("\n")

    # 5.sendcost发货退货数集合到一起 写入数据库
    sendcost_countlist = []
    for k, y in send_shop_dict.items():
        for k1, y1 in y.items():
            temp = {'shop': k, 'now_date': date, 'stylecode': k1, 'send_number': y1, "is_delete": 0,
                    'today_price': get_today_cost(stylecode=k1), "refund_number": 0}
            # print(f"发货新增:{temp}")
            sendcost_countlist.append(temp)

    for k, y in refund_shop_dict.items():
        for k1, y1 in y.items():
            cr = 0
            for i in sendcost_countlist:
                if k == i['shop'] and k1 == i['stylecode']:
                    i['refund_number'] = y1
                    cr = 1
            if cr == 0:
                # print(k1)
                sendcost_countlist.append(
                    {'shop': k, 'now_date': date, 'stylecode': k1, 'send_number': 0, "is_delete": 0,
                     'today_price': get_today_cost(stylecode=k1), "refund_number": y1})
    print(sendcost_countlist)
    # 循环写入数据库 send_cost
    for i in sendcost_countlist:
        sql_cls = mysql_config()
        sql = f"insert into dy_sendcost values(null,'{i['shop']}','{i['now_date']}','{i['stylecode']}',{i['send_number']},{i['today_price']},0,{i['refund_number']})"
        rs = sql_cls.sql_commit(sql)
        if rs:
            print("sendcost写入成功")
        else:
            print("sendcost SQL持久化错误")
        sql_cls.close_db()


#读取补单文件夹中拼多多补单数据
def get_budan_price(path):
    return_dict={}
    # path=r"../BD_DATA/财务补单数据.xlsx"
    data=read_xlsx(path=path,sheet_name="拼多多 京东 抖音",header_line=1)
    for i in data:
        if i[0]==None or i[1]==None or i[2]==None or i[3]==None:
            continue
        cur_date=xlrd.xldate.xldate_as_datetime(i[0], 0).strftime("%Y-%m-%d")
        if cur_date not in return_dict:
            return_dict[cur_date]={}
        shop_name = i[1]#.replace("'", "")
        return_dict[cur_date][shop_name]={'budan_price':i[2],'budan_yongjin':i[3]}
    return return_dict

#将补单数据存入sales表
def import_budan_data(date,path):
    budan_data_dict=get_budan_price(path=path)
    #循环今天补单数据
    for k,y in budan_data_dict[date].items():
        print(k,y)
        sql_cls = mysql_config()
        sql = f"update dy_sales set budan_price={float(y['budan_price'])} where shop='{k}' and now_date='{date}'"
        rs = sql_cls.sql_commit(sql)
        if rs:
            print(f"{date}补单金额,写入成功")
            pass
        else:
            print(f"{date}补单金额,SQL持久化错误{k}")
        sql_cls.close_db()
