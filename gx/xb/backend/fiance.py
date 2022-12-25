import pandas as pd
import numpy as np
import os
import csv
#function
def read_csv(path, header_line=1):
    try:
        with open(path, encoding="gbk") as f:
            reader = csv.reader(f)
            data = [list(item) for item in reader]
            data = data[header_line:]
            return data
    except:
        with open(path, encoding="ANSI") as f:
            reader = csv.reader(f)
            data = [list(item) for item in reader]
            data = data[header_line:]
            return data
#取销售主题表需要的字段
def get_Sales_needField(info_list):
    return_list=[]
    for i in info_list:
        temp=[
            i[0],#内部订单号
            i[1],#标记多标签
            i[8],#店铺
            i[31],#款式编码
            i[30],#商品编码
            i[38],#商品名称
            i[46],# 销售数量
            i[49],# 实发数量
            i[50],# 实发金额
            i[51],# 销售金额
            i[52],# 销售成本
            i[53],# 实发成本
            i[56],# 已付金额
            i[57],# 应付金额
            i[60],# 退货数量
            i[61],# 实退数量
            i[62],# 退货金额
            i[63],# 退货成本
            i[64],# 实退成本
            i[65]# 实退金额
        ]
        return_list.append(temp)
    return return_list
#取售后主题表需要的字段
def get_AfterSales_needField(info_list):
    return_list=[]
    for i in info_list:
        temp=[
            i[1],#内部订单号
            i[10],#店铺
            i[24],#商品编码
            i[25],#款式编码
            i[35],#退货数量
            i[36],#实退数量
            i[37],#退货金额
            i[38],#实退金额
            i[39],#退货成本金额
            i[40]#实退成本金额
        ]
        return_list.append(temp)
    return return_list
#取进销存表需要的字段()
def get_Invoicing_needField(info_list):
    return_list=[]
    for i in info_list:
        return_list.append(i[1])
    return_list=list(set(return_list))
    return return_list
def Sales_cleaning1(info_list,invoicing_list):
    #列表长度18
    #['21949197', '【异常大单】,【补单】仓库不发货,多多批发,特殊单,线上发货', "PDD女装-I'M DAVID小布家", 'XL-男女毛圈开衫-米色-饼干们_KB-CP', '5', '0', '', '0.01', '189.85', '', '0.01', '0.01', '', '', '', '', '', '']
    #内部订单号、标记多标签、店铺,款式编码,商品编码、商品名称、销售数量、实发数量、实发金额、销售金额、销售成本、实发成本、已付金额、应付金额、退货数量、实退数量、退货金额、退货成本、实退成本、实退金额
    #一次处理
    for i in info_list:
        if "特殊单" in i[1]:
            i.append("特殊单")
        elif "【补单】发福袋" in i[1]:
            i.append("特殊单发福袋")
        elif "买家秀" in i[1]:
            i.append("买家秀")
        elif "补单" in i[1]:
            i.append("正常单打成特殊单")
        else:
            i.append("正常单")
    #二次处理
    for i in info_list:
        if "YFLJ" in i[3]:
            i.append("邮费")
        elif "白坯" in i[3]:
            i.append("白坯")
        elif "DF" in i[3]:
            i.append("代发")
        elif "HCY" in i[3]:
            i.append("代发")
        elif "NQ" in i[3]:
            i.append("代发")
        elif "烫画" in i[3]:
            i.append("烫画")
        elif "DS" in i[3]:
            i.append("代发")
        elif "HC" in i[3]:
            i.append("代发")
        elif "辅料" in i[3]:
            i.append("辅料")
        elif "运费补差价" in i[3]:
            i.append("邮费")
        elif "邮费" in i[3]:
            i.append("邮费")
        elif "-CP" in i[4]:
            i.append("CP")
        elif "-福袋" in i[4]:
            i.append("福袋")
        else:
            i.append("")
    in_list=",".join(invoicing_list)
    #三次处理
    for index,i in enumerate(info_list):
        print(index)
        if i[0] in in_list:
            i.append("已出库")
        else:
            i.append("")
    return info_list

#售后数据处理
def AfterSales_cleaning1(info_list,invoicing_list):
    #二次处理
    for i in info_list:
        if "YFLJ" in i[3]:
            i.append("邮费")
        elif "白坯" in i[3]:
            i.append("白坯")
        elif "DF" in i[3]:
            i.append("代发")
        elif "HCY" in i[3]:
            i.append("代发")
        elif "NQ" in i[3]:
            i.append("代发")
        elif "烫画" in i[3]:
            i.append("烫画")
        elif "DS" in i[3]:
            i.append("代发")
        elif "HC" in i[3]:
            i.append("代发")
        elif "辅料" in i[3]:
            i.append("辅料")
        elif "运费补差价" in i[3]:
            i.append("邮费")
        elif "邮费" in i[3]:
            i.append("邮费")
        elif "-CP" in i[2]:
            i.append("CP")
        elif "-福袋" in i[2]:
            i.append("福袋")
        else:
            i.append("")
    in_list = ",".join(invoicing_list)
    #三次处理
    for i in info_list:
        if i[0] in in_list:
            i.append("已出库")
        else:
            i.append("")
    return info_list
#main
jxc_path = r"C:\Users\hwj\Desktop\00--4月销售主体分析\进销存"
zt_path=r"C:\Users\hwj\Desktop\00--4月销售主体分析\销售主题分析"
sh_path=r"C:\Users\hwj\Desktop\00--4月销售主体分析\售后主题分析"
def get_data(path):
    jxc_data = []
    for i in os.listdir(path):
        if i.split(".")[-1]=="csv":
            cur_url=os.path.join(path,i)
            data=read_csv(cur_url)
            jxc_data.extend(data)
    file_name=path.split('\\')[-1]
    print(f"{file_name}数据条数:  {len(jxc_data)}")
    return jxc_data

jxc=get_data(jxc_path)
zt=get_data(zt_path)
sh=get_data(sh_path)

print(jxc[0])
print(zt[0])
print(sh[0])
#1.摘除 销售主题分析 不需要的字段
print("开始摘除销售主题分析")
zt=get_Sales_needField(zt)
#2.摘除 售后主题分析 不需要的字段
print("开始摘除售后主题分析")
sh=get_AfterSales_needField(sh)
#3.摘除 进销存 不需要的字段
print("开始摘除进销存")
jxc=get_Invoicing_needField(jxc)
print("摘除完了之后长度:{}".format(len(jxc)))

#4.销售主题分析 清洗1
zt=Sales_cleaning1(info_list=zt,invoicing_list=jxc)
zt_data_header=["内部订单号","标记多标签","店铺","款式编码","商品编码","商品名称","销售数量","实发数量","实发金额","销售金额","销售成本","实发成本","已付金额","应付金额","退货数量","实退数量","退货金额","退货成本","实退成本","实退金额","分类列1","分类列2","分类列3"]
print(f"主题销售分析结果长度{len(zt)}")

#5.售后主题分析 清洗1
sh=AfterSales_cleaning1(info_list=sh,invoicing_list=jxc)
sh_data_header=["内部订单号","店铺","商品编码","款式编码","退货数量","实退数量","退货金额","实退金额","退货成本金额","实退成本金额","分类列1","分类列2"]
print(f"主题销售分析结果长度{len(sh)}")

print("开始写入销售主题结果")
with open("销售主题_结果.csv-1","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator='\n')
    writer.writerow(zt_data_header)
    writer.writerows(zt[:500000])

with open("销售主题_结果.csv-2","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator='\n')
    writer.writerow(zt_data_header)
    writer.writerows(zt[500000:])

print("开始写入售后主题结果")
with open("售后主题_结果.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator='\n')
    writer.writerow(sh_data_header)
    writer.writerows(sh)




