import requests
import time

from dy_get_data.dy_exts import *
from exts import *
class dy_doudian:#抖店数据

    def __init__(self,cookies):
        self.requests=requests.session()
        self.cookies=cookies
        self.setCookies()

    def convert_cookies_to_dict(self):
        self.cookies = dict([l.split("=", 1) for l in self.cookies.split("; ")])

    def setCookies(self):
        if type(self.cookies) == str:
            self.convert_cookies_to_dict()
        requests.utils.add_dict_to_cookiejar(self.requests.cookies,self.cookies)

    #获取成交退款
    def get_cjtk(self,date):
        start_time=time.strptime(date+" 00:00:00",'%Y-%m-%d %H:%M:%S')
        end_time = time.strptime(date + " 23:59:59",'%Y-%m-%d %H:%M:%S')
        start_time_stamp = int(time.mktime(start_time))
        end_time_stamp = int(time.mktime(end_time))
        responce = self.requests.get(
            url=f"https://compass.jinritemai.com/business_api/shop/homepage/market_trend?visual_type=1&index_selected=pay_amt%2Crefund_amt&date_type=2&begin_date={start_time_stamp}&end_date={end_time_stamp}&is_activity=false",
            headers=DY_CJTK_HEADERS)
        res_json = responce.json()
        if res_json['st'] == 0:
            now_date=res_json['data']['data_result']['value'][0]['x']
            cj_price=round(res_json['data']['data_result']['value'][0]['y']['pay_amt']/100,2)
            tk_price=round(res_json['data']['data_result']['value'][0]['y']['refund_amt']/100,2)
            return {'status':100,'msg':'获取成交退款成功','data':{'now_date':now_date,'cj_price':cj_price,'tk_price':tk_price}}
        else:
            return {'status':-1,'msg':'获取成交退款失败','data':responce.json()}

    # 获取成交退款多天
    def get_cjtk_manyday(self,start_date, end_date):
        start_time = time.strptime(start_date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_time = time.strptime(end_date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        start_time_stamp = int(time.mktime(start_time))
        end_time_stamp = int(time.mktime(end_time))
        responce = self.requests.get(
            url=f"https://compass.jinritemai.com/business_api/shop/homepage/market_trend?visual_type=1&index_selected=pay_amt%2Crefund_amt&date_type=2&begin_date={start_time_stamp}&end_date={end_time_stamp}&is_activity=false",
            headers=DY_CJTK_HEADERS)
        res_json = responce.json()
        cj_count=0
        tk_count=0
        if res_json['st'] == 0:
            for i in res_json['data']['data_result']['value']:
                now_date=i['x']
                cj_price=round(i['y']['pay_amt']/100,2)
                tk_price=round(i['y']['refund_amt']/100,2)
                cj_count+=cj_price
                tk_count+=tk_price
                # print(now_date,cj_price,tk_price)
            return {'status': 100, 'msg': '获取成交退款成功',
                    'data': {'now_date': f"{res_json['data']['data_result']['value'][0]['x']}-{res_json['data']['data_result']['value'][-1]['x']}",
                             'cj_price': round(cj_count,2), 'tk_price': round(tk_count,2)}}
        else:
            return {'status': -1, 'msg': '获取成交退款失败', 'data': responce.json()}

    #获取运费险
    def get_yfx(self,date):
        data_list=[]
        for i in range(0,1000):
            responce = self.requests.get(
                url=f"https://fxg.jinritemai.com/shop/be/settlement/settlement/shopAccountBillItems?page={i}&page_size=200&time_type=BILL_TIME&start_time={date}+00:00:00&end_time={date}+23:59:59",
                headers=DY_YFX_HEADERS)
            res_json=responce.json()
            if res_json['msg'] == 'success' and res_json['st'] == 0:
                if len(res_json['data'])==0:
                    break
                else:
                    data_list+=res_json['data']
            else:
                return {'status': -1, 'msg': '获取运费险失败', 'data': responce.json()}
        yfx = 0
        send_timeout=0
        collect_timeout=0
        fake_send_timeout=0
        violation=0
        small_pay=0
        daren_yongjin=0
        mrketing=0
        for i in data_list:
            if '运费险扣减' in i['account_bill_desc']:
                yfx += float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "国内发货超时" in i['account_bill_desc']:
                send_timeout+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "国内揽收超时" in i['account_bill_desc']:
                collect_timeout+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "国内虚假发货发运超时" in i['account_bill_desc']:
                fake_send_timeout+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "奖惩中心严重违规" in i['account_bill_desc']:
                violation+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "小额打款" in i['account_bill_desc']:
                small_pay+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "达人带货佣金" in i['account_bill_desc']:
                daren_yongjin+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
            if "营销费用划扣" in i['account_bill_desc']:
                mrketing+=float(i['account_amount']) if i['fund_flow']=="出账" else -float(i['account_amount'])
        yfx = round(yfx / 100, 2)
        send_timeout = round(send_timeout / 100, 2)
        collect_timeout = round(collect_timeout / 100, 2)
        fake_send_timeout = round(fake_send_timeout / 100, 2)
        violation = round(violation / 100, 2)
        small_pay = round(small_pay / 100, 2)
        daren_yongjin = round(daren_yongjin / 100, 2)
        mrketing=round(mrketing /100, 2)

        return {'status':100,'msg':'获取运费险成功','data':
            {"yfx":yfx,
             "send_timeout":send_timeout,
             "collect_timeout": collect_timeout,
             "fake_send_timeout": fake_send_timeout,
             "violation": violation,
             "small_pay": small_pay,
             "daren_yongjin":daren_yongjin,
             "mrketing":mrketing
             }}

    #获取资金账单 月度账单各个类型 余额
    def get_bill(self,start_date,end_date,type):
        start_time = time.strptime(start_date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_time = time.strptime(end_date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        start_time_stamp = int(time.mktime(start_time))
        end_time_stamp = int(time.mktime(end_time))
        url=f'https://fxg.jinritemai.com/settlement/settlement/shopAccountBill?page=0&page_size=10&start_time={start_time_stamp}&end_time={end_time_stamp}&period_type=MONTH&account_type={type}'
        response=self.requests.get(url=url,headers=DY_MONTH_DATA_HEADERS)
        res_json=response.json()
        if res_json['st']==0:
            if len(res_json['data'])==0:
                return None
            else:
                cur_data=res_json['data'][0]
                re_dict={
                    'bill_date': cur_data['bill_date'],#日期 月
                     'detail_count': cur_data['detail_count'],#明细笔数
                     'income': round(cur_data['income']*0.01,2),#总收入
                     'outcome': round(cur_data['outcome']*0.01,2),#总支出
                     'net_earning': round(cur_data['net_earning']*0.01,2),#余额变化
                     'beginning_balance': round(cur_data['beginning_balance']*0.01,2),#期初余额
                     'ending_balance': round(cur_data['ending_balance']*0.01,2),#期末余额
                     'begin_date': cur_data['begin_date'],#开始日期
                     'end_date': cur_data['end_date'],#结束日期
                     'account_type': cur_data['account_type']#选择类型
                }
                return re_dict
        else:
            print("抖音获取月度账单请求失败!")
            raise ValueError('数据请求出现问题')

    #下载月度报表
    def download_month_table(self,shop_name,download_id,start_date,end_date):
        url=f'https://fxg.jinritemai.com/settlement/settlement/downloadFileFromId?download_id={download_id}'
        response=self.requests.get(url=url,headers=DY_MONTH_DOWNTABLE_HEADERS)
        res_json = response.json()
        if res_json['st'] != 0:
            return None
        else:
            try:
                down_http=res_json['data']['url']
            except:
                time.sleep(5)
                down_http = res_json['data']['url']
            http_content=self.requests.get(url=down_http)
            current_path = join_path(f"DY_MONTH_DATA\\{shop_name}-DY月账单流水{start_date}-{end_date}.xlsx")
            with open(current_path, "wb") as f:
                f.write(http_content.content)
                print(f"{shop_name}下载成功")

    #获取月自己账号明细表
    def get_month_table(self,shop_name,start_date,end_date):
        start_time = time.strptime(start_date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_time = time.strptime(end_date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        start_time_stamp = int(time.mktime(start_time))
        end_time_stamp = int(time.mktime(end_time))
        url=f'https://fxg.jinritemai.com/settlement/settlement/downloadItemV2'
        data={
            'start_time':start_time_stamp,
            'end_time': end_time_stamp,
            'account_type':'',
            'time_type':'BILL_TIME'
        }
        response=self.requests.post(url=url,headers=DY_MONTH_TABLE_HEADERS,data=data)
        res_json = response.json()
        if res_json['st'] != 0:
            return None
        else:
            print(f"{shop_name}-月度报表获取成功!")
            time.sleep(5)#等待报表生成
            self.download_month_table(shop_name,res_json['data'],start_date,end_date)











