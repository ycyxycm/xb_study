from dy_get_data.dy_data import dy_doudian
from util.mysqlConfig import mysql_config
from threading import Thread


#获取抖音平台  店铺的cookies
def get_cookies():
	mysql_obj=mysql_config()
	sql="select * from cookies_all where Shop_pallet='抖音'"
	res=mysql_obj.sql_fetch(sql)
	cookie_list=[list(i) for i in res]
	mysql_obj.close_db()
	return cookie_list

#遍历cookies抓取数据[{'id': 10, 'Shop': 'DY-LOG潮牌个体店', 'Shop_pallet': '抖音', 'cookies': 'ckvalue', 'update_time': '2022-10-25T09:49:51'}]
def use_ck_getdata(cookies_list,date):
	return_list=[]
	for i in cookies_list:
		print(i[0])
		temp_dict={}
		mycls=dy_doudian(cookies=i[2])
		cur_data=mycls.get_yfx(date=date)
		cjtk = mycls.get_cjtk(date=date)
		if cur_data['status']!=100:
			raise ValueError(cur_data['msg'],cur_data['data'])
		elif cjtk['status']!=100:
			raise ValueError(cjtk['msg'], cjtk['data'])
		temp_dict['shop']=i[0]
		temp_dict['deal_price']=cjtk['data']['cj_price']
		temp_dict['refund_price'] = cjtk['data']['tk_price']
		temp_dict['now_date'] = date
		temp_dict["budan_price"]=0.00
		temp_dict["budan_yongjin"]=0.00
		temp_dict["extension_price"]=0.00
		temp_dict["kf_re_price"]=0.00

		temp_dict['freight'] = cur_data['data']['yfx']
		temp_dict["send_timeout"] = cur_data['data']['send_timeout']
		temp_dict["collect_timeout"] = cur_data['data']['collect_timeout']
		temp_dict["fake_send_timeout"] = cur_data['data']['fake_send_timeout']
		temp_dict["violation"] = cur_data['data']['violation']
		temp_dict["small_pay"] = cur_data['data']['small_pay']
		temp_dict['daren_yongjin']=cur_data['data']['daren_yongjin']
		temp_dict['mrketing'] = cur_data['data']['mrketing']

		return_list.append(temp_dict)
	return return_list

#

#循环写入数据库
def add_database(date):
	cookies_list = get_cookies()  # 从数据库获取所有抖店cookies
	dy_list = use_ck_getdata(cookies_list=cookies_list, date=date)  # 遍历cookies抓取店铺数据
	for i in dy_list:
		mysql_obj=mysql_config()
		sql=f"select * from dy_sales where shop='{i['shop']}' and now_date='{i['now_date']}'"
		r1=mysql_obj.sql_fetch(sql)
		if len(r1)>0:
			print(f"{i['shop']}---{i['now_date']}--当天数据已存在 已跳过")
		else:
			sql=f"insert into dy_sales values(null,'{i['shop']}','{i['now_date']}',{i['deal_price']},{i['refund_price']},{i['freight']},0,0,0,0,0,{i['collect_timeout']},{i['fake_send_timeout']},{i['send_timeout']},{i['small_pay']},{i['violation']},{i['daren_yongjin']},{i['mrketing']})"
			rs=mysql_obj.sql_commit(sql)
			if rs:
				print(f"{i['shop']}---{i['now_date']}--数据存入数据库成功")
			else:
				print(f"{i['shop']}---{i['now_date']}--SQL持久化出现问题")

#############################################################
def dy_download_main(start_date,end_date):
	cookies_list = get_cookies()  # 从数据库获取所有抖店cookies
	task=[]#进程池
	for i in cookies_list:
		ts=Thread(target=dy_download_month_table,args=(i[0],i[2],start_date,end_date,))
		task.append(ts)
	for i in task:
		i.start()
	for i in task:
		i.join()

def dy_download_month_table(shop_name,cookie,start_date,end_date):
	a = dy_doudian(cookies=cookie)
	a.get_month_table(shop_name, start_date=start_date, end_date=end_date)
##############################################################


def get_month_date_dy(start_date,end_date):
	# 抖店月度数据
	cookies_list = get_cookies()
	all_list = []
	simple_list = []
	for i in cookies_list:
		mycls = dy_doudian(i[2])
		# #账户余额
		cur_count = mycls.get_cjtk_manyday(start_date=start_date,
										   end_date=end_date)  # {'status': 100, 'msg': '获取成交退款成功', 'data': {'now_date': '10/01-10/31', 'cj_price': 140332.82, 'tk_price': 46819.030000000006}}
		dy_month_date = {}  # {'shop': 'DY-LOG潮牌个体店', 'date': '10/01-10/31', 'month_cj': 113686.69, 'month_tk': 39364.0, 'ALL': {'bill_date': '2022-09', 'detail_count': 1333, 'income': 22294.15, 'outcome': 1904.81, 'net_earning': 20389.34, 'beginning_balance': 0.0, 'ending_balance': 20389.34, 'begin_date': '2022-09-01 00:00:00', 'end_date': '2022-09-30 23:59:59', 'account_type': 'ALL'}, 'WX': {'bill_date': '2022-09', 'detail_count': 505, 'income': 8860.57, 'outcome': 0.0, 'net_earning': 8860.57, 'beginning_balance': 0.0, 'ending_balance': 8860.57, 'begin_date': '2022-09-01 00:00:00', 'end_date': '2022-09-30 23:59:59', 'account_type': 'WX'}, 'NEW_ZFB': None, 'ZFB': None, 'HZ': None, 'PA': {'bill_date': '2022-09', 'detail_count': 828, 'income': 13433.58, 'outcome': 1904.81, 'net_earning': 11528.77, 'beginning_balance': 0.0, 'ending_balance': 11528.77, 'begin_date': '2022-09-01 00:00:00', 'end_date': '2022-09-30 23:59:59', 'account_type': 'PA'}}
		dy_month_simple = []  # ['shop','date','month_cj','month_tk','all_期末余额','WX_期末余额','NEWZFB_期末余额','ZFB_期末余额','抖音_期末余额','聚合_期末余额']

		dy_month_date['shop'] = i[0]
		dy_month_date['date'] = cur_count['data']['now_date']
		dy_month_date['month_cj'] = cur_count['data']['cj_price']
		dy_month_date['month_tk'] = cur_count['data']['tk_price']

		dy_month_simple.append(i[0])
		dy_month_simple.append(cur_count['data']['now_date'])
		dy_month_simple.append(cur_count['data']['cj_price'])
		dy_month_simple.append(cur_count['data']['tk_price'])

		for j in ['', 'WX', 'NEW_ZFB', 'ZFB', 'HZ', 'PA']:  # ''=所有支付方式 WX=微信 NEW_ZFB=支付宝-生效中 ZFB=支付宝 HZ=抖音支付 PA=聚合支付
			cur = mycls.get_bill(start_date=start_date, end_date=end_date, type=j)
			if j == '':
				j_name = "ALL"
			else:
				j_name = j
			dy_month_date[j_name] = cur
			if cur is None:
				dy_month_simple.append(0)
			else:
				dy_month_simple.append(cur['ending_balance'])
		simple_list.append(dy_month_simple)
		all_list.append(dy_month_date)

	# print(simple_list)
	return simple_list
