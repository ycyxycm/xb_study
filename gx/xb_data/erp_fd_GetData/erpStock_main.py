
import os

from erp_fd_GetData.erp_data import erp_stock
from util.mysqlConfig import mysql_config

#通过cookie分辨男女仓库 将获取到的数据存入数据库
def sql_stock_date(cookies):
    sql_cls=mysql_config()
    #实例化抓取类
    es=erp_stock(cookies=cookies)
    stock_data_all=es.get_male_stock()
    #列表去重 数量重算
    cur_dict={}
    for i in stock_data_all:
        if '福袋' in i['sku_id']:
            continue
        if i['sku_id'] not in cur_dict.keys():
            cur_dict[i['sku_id']]={"i_id":i['i_id'],"qty":i['qty']}
        else:
            cur_dict[i['sku_id']]['qty']+=i['qty']
    #循环入库
    for k,y in cur_dict.items():
        sql=f"insert into erp_male_stock values('{k}','{y['i_id']}',{y['qty']})"
        r_type=sql_cls.sql_commit(sql)
        if r_type:
            pass
        else:
            print("写入mysql失败 {}".format(k,y))
            raise ValueError("写入mysql失败 {}".format(k,y))
    print("金桥仓 成品装写入成功!")


#通过cookie分辨男女仓库 将获取到的数据存入数据库
def female_sql_stock_date(cookies):
    sql_cls=mysql_config()
    #实例化抓取类
    es=erp_stock(cookies=cookies)
    stock_data_all=es.get_female_stock()
    #列表去重 数量重算
    cur_dict={}
    for i in stock_data_all:
        if '福袋' in i['sku_id']:
            continue
        if i['sku_id'] not in cur_dict.keys():
            cur_dict[i['sku_id']]={"i_id":i['i_id'],"qty":i['qty']}
        else:
            cur_dict[i['sku_id']]['qty']+=i['qty']
    #循环入库
    for k,y in cur_dict.items():
        sql=f"insert into erp_female_stock values('{k}','{y['i_id']}',{y['qty']})"
        r_type=sql_cls.sql_commit(sql)
        if r_type:
            pass
        else:
            print("写入mysql失败 {}".format(k,y))
            raise ValueError("写入mysql失败 {}".format(k,y))
    print("女装主仓 成品装写入成功!")
