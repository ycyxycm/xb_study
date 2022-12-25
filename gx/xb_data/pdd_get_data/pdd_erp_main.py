from util.mysqlConfig import mysql_config
import xlrd

from exts import *
from pdd_get_data.pdd_erp_data import erp_info
from util.myredis import RedisClient


#1.pdd主题分析表筛选
def filter_data(data_counts):
    new_data_counts=[]
    for i in data_counts:# 筛选
        # 店铺带 ' 的替换为空
        if i['店铺'] is None:
            continue
        else:
            i['店铺'] = i['店铺'].replace("'", "")

        #标记多标签：补单关键字全部删掉
        if i["标记多标签"] is None:
            pass
        elif '补单' in i["标记多标签"]:
            if '未设定' in i['发货仓']:#补单没发货
                continue
            else:#补单发货
                i['款式编码']="补单发货编码"


        #订单类型:去掉所有换货订单
        if i['订单类型'] is None:
            pass
        elif '换货订单' in i['订单类型']:
            continue

        # 线上商品名：无须，无需，差价。带这几个关键字的就删掉
        if i['线上商品名'] is None:
            pass
        elif "无需" in i['线上商品名'] or "无须" in i['线上商品名'] or "差价" in i['线上商品名']:
            continue


        # 款式编码：烫画，白坯，白胚两个字替换空，辅料用前面的商品编码填充过去
        if i['款式编码'] is None:
            pass
        elif "烫画" in i['款式编码']:
            continue

        if i['款式编码'] is None:
            pass
        elif "白坯" in i['款式编码'] or "白胚" in i['款式编码']:
            i['款式编码']=i['款式编码'].replace("白坯","").replace("白胚","")

        new_data_counts.append(i)
    return new_data_counts

#1.售后主题分析筛选
def sh_filter_data(data_counts):
    new_data_counts = []
    for i in data_counts:  # 筛选
        # 店铺带 ' 的替换为空
        if i['店铺'] is None:
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
        elif "-" in i['款式编码']:
            i['款式编码']=i['款式编码'].split("-")[1]
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

#4.查询PDD当天成本价(拼多多)
def get_today_cost(stylecode):
    mycls=mysql_config()
    sql=f'select * from finace_cost where stylecode="{stylecode}"'
    res=mycls.sql_fetch(sql)
    if len(res)==0:
        raise ValueError(f"成本价查询失败,建议将send_cost表今日数据删除重新跑---{stylecode}")
    else:
        return res[0][3]

#4.查询PDD当天吊牌价(拼多多)
def get_today_tag(shop,stylecode):
    mycls=mysql_config()
    sql=f'select * from finace_tag_price where shop="{shop}"'
    res=mycls.sql_fetch(sql)
    if len(res)==0:
        raise ValueError(f"吊牌价查询失败,建议将send_cost表今日数据删除重新跑---{shop}---{stylecode}")
    else:#{'shop':res[0][0],'male_tag':res[0][1],'famale_tag':res[0][2],'child_tag':res[0][3]}
        if get_now_sex(stylecode)==1:
            return res[0][1]
        elif get_now_sex(stylecode)==0:
            return res[0][2]
        elif get_now_sex(stylecode)==2:
            return res[0][3]

def pdd_sh_main(cookies,date):
    mycls=erp_info(cookies=cookies)

    refund_data_counts=mycls.get_pdd_shztfx_table(date)#获取售后主题分析
    print(f"开始对售后分析表进行筛选  筛选前 {len(refund_data_counts)} 条")
    refund_data_counts=sh_filter_data(data_counts=refund_data_counts)#1.对售后分析表进行筛选
    print(f"售后分析 筛选后的数据计 {len(refund_data_counts)} 条")
    print("\n")

    #3.统计各个店铺各个款式的退货数量
    print("统计各个店铺各个款式的退货数量")
    refund_shop_dict=count_refundshop(data_counts=refund_data_counts)
    print(refund_shop_dict)
    print("\n")
    return refund_shop_dict


def pdd_zt_main(cookies, date):
    mycls = erp_info(cookies=cookies)

    data_counts = mycls.get_pdd_ztxsfx_table(date)  # 获取主题分析表
    print(f"开始对主题分析表进行筛选  筛选前 {len(data_counts)} 条")
    data_counts = filter_data(data_counts=data_counts)  # 1.对主题分析表进行筛选
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
    return {'orders_count_dict': orders_count_dict, 'send_shop_dict': send_shop_dict}


def pdd_sql_main(date,erp_cookies):
    try:
        refund_shop_dict = pdd_sh_main(cookies=erp_cookies, date=date)
        zt_dict = pdd_zt_main(cookies=erp_cookies, date=date)
        orders_count_dict = zt_dict['orders_count_dict']
        send_shop_dict = zt_dict['send_shop_dict']

        # SQL
        # PDD店铺订单数写入数据库{'PDD男装-JEANSWEST真维斯休闲装旗舰店': 266, 'PDD男装-雪中飞小布家专卖店': 6, 'PDD女装-雪中飞飘思芬专卖店': 572, "PDD女装-I'M DAVID小布家": 351, "PDD女装-I'MDAVID禾季纯专卖店": 505, 'PDD女装-雪中飞阅香时代专卖店': 211, 'PDD女装-玩未锐越专卖店': 3, 'PDD女装-蓝卓恩官方旗舰店': 50, 'PDD女装-真维斯阅香时代专卖店': 110, 'PDD女装-真维斯较真专卖店': 166, 'PDD女装-语霖旗舰店': 23, 'PDD男装-布衣不二旗舰店': 1, 'PDD童装-田芽旗舰店': 6, 'PDD童装-高梵麦威伦店': 6, 'PDD女装-叮当制造官方旗舰店': 5}
        print("#######################开始写入拼多多订单数据#################################")
        for k, y in orders_count_dict.items():
            sql_cls = mysql_config()
            sql = f"insert into pdd_sendgoods values(null,'{k}','{date}',{y},0)"
            rs = sql_cls.sql_commit(sql)
            if rs:
                print(f"店铺{k},日期{date},写入数据库成功")
            else:
                print(f"店铺{k},日期{date},SQL持久化出错")
            sql_cls.close_db()
        print("\n")

        # PDD各个款式 发货数量 退货数量写入数据库
        sendcost_countlist = []
        for k, y in send_shop_dict.items():
            for k1, y1 in y.items():
                temp = {'shop': k, 'now_date': date, 'stylecode': k1, 'send_number': y1, "is_delete": 0,
                        'today_price': get_today_cost(stylecode=k1), "refund_number": 0,
                        'today_tag':0 if get_today_tag(shop=k, stylecode=k1) is None else get_today_tag(shop=k, stylecode=k1) }
                sendcost_countlist.append(temp)

        for k, y in refund_shop_dict.items():
            for k1, y1 in y.items():
                cr = 0
                for i in sendcost_countlist:
                    if k == i['shop'] and k1 == i['stylecode']:
                        i['refund_number'] = y1
                        cr = 1
                if cr == 0:
                    temp = {'shop': k, 'now_date': date, 'stylecode': k1, 'send_number': 0, "is_delete": 0,
                            'today_price': get_today_cost(stylecode=k1), "refund_number": y1,
                            'today_tag':0 if get_today_tag(shop=k, stylecode=k1) is None else get_today_tag(shop=k, stylecode=k1)}
                    sendcost_countlist.append(temp)
        print(sendcost_countlist)

        #######################开始写入拼多多退货数据#################################
        # 循环写入数据库 send_cost
        for i in sendcost_countlist:
            sql_cls = mysql_config()
            sql = f"insert into pdd_sendcost values(null,'{i['shop']}','{i['now_date']}','{i['stylecode']}',{i['send_number']},{i['refund_number']},{i['today_price']},{i['today_tag']},0)"
            rs = sql_cls.sql_commit(sql)
            if rs:
                print("sendcost写入成功")
                pass
            else:
                print("sendcost SQL持久化错误{}".format(i))
            sql_cls.close_db()
        #修改redis数据库 当天数据流程状态
        cur_date_number = date.replace("-", "")
        cur_index = int(cur_date_number +  str(2))#2号位
        try:
            rds=RedisClient()
            bitname="pdd_date_status"#拼多多日报数据流程情况
            rds.client.setbit(name=bitname,offset=cur_index,value=1)
            print("redis写入2号位状态成功")
        except:
            print("redis写入2号位状态失败")
    except Exception as e:
        print("拼多多订单数量 款式发退货写入数据库错误")
        print(e)

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
        shop_name = i[1].replace("'", "")
        return_dict[cur_date][shop_name]={'budan_price':i[2],'budan_yongjin':i[3]}
    return return_dict

#将补单数据存入sales表
def import_budan_data(date,path):
    budan_data_dict=get_budan_price(path=path)
    #循环今天补单数据
    for k,y in budan_data_dict[date].items():
        print(k,y)
        sql_cls = mysql_config()
        sql = f"update pdd_sales set budan_price={float(y['budan_price'])},budan_yongjin={float(y['budan_yongjin'])} where shop='{k}' and now_date='{date}'"
        rs = sql_cls.sql_commit(sql)
        if rs:
            print(f"{date}补单金额,写入成功")
            pass
        else:
            print(f"{date}补单金额,SQL持久化错误{k}")
        sql_cls.close_db()

    # sql_cls = mysql_config()

