import os

import openpyxl

from dy_get_data import dy_main,dy_erp_main
from exts import join_path,save_file
from pdd_get_data import pdd_erp_main
from erp_fd_GetData import erpStock_main
from dy_get_data.dy_data import dy_doudian

erp_cookies="XXX"


'''
    抖音日报
'''
date="2022-12-22"
# 抖音主题 售后分析数据并写入数据库
# dy_erp_main.dy_sql_main(erp_cookies=erp_cookies,date=date)
# 抖店数据抓取
dy_main.add_database(date=date)#抖店数据写入数据库

# 抖音 补单数据获取
print(os.path.join(os.getcwd(),"BD_DATA/财务补单数据.xlsx"))
dy_erp_main.import_budan_data(date,os.path.join(os.getcwd(),"BD_DATA/财务补单数据.xlsx"))



'''
    拼多多日报
'''
# # 拼多多主题 售后分析
# date='2022-12-22'
# pdd_erp_main.pdd_sql_main(erp_cookies=erp_cookies,date=date)
# # 拼多多 补单数据获取
# # print(os.path.join(os.getcwd(),"BD_DATA/财务补单数据.xlsx"))
# pdd_erp_main.import_budan_data(date=date,path=os.path.join(os.getcwd(),"BD_DATA/财务补单数据.xlsx"))


'''
    抖音月报
'''
# #获取抖店月资金
# start_date="2022-11-01"
# end_date="2022-11-30"
# month_date_list=dy_main.get_month_date_dy(start_date=start_date,end_date=end_date)#获取月度数据
# month_date_list.insert(0,['店铺','日期','月成交','月退款','所有类型期末余额','微信期末余额','支付宝-生效中期末余额','生效中期末余额','抖音期末余额','聚合支付期末余额'])#添加标头
# print(month_date_list)
#
# current_path = join_path(f"DY_MONTH_DATA\\DY月账单期末余额{start_date}-{end_date}.xlsx")#写入路径
# save_file(month_date_list,current_path)#写入
#
# # 获取抖店月账单明细
# dy_main.dy_download_main(start_date=start_date,end_date=end_date)



'''
    ERP箱及仓位库存录入
'''
# # 男装仓
# jinqiaocang_cookies="XXX"
# erpStock_main.sql_stock_date(cookies=jinqiaocang_cookies)#金桥仓库成品装写入数据库
# # 女装主仓
# erpStock_main.female_sql_stock_date(cookies=erp_cookies)