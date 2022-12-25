import logging
import os
import time
from lxml import etree
import requests,json
from urllib.parse import quote_plus
from threading import Thread

from backend import settings


class erp_stock:#ERP福袋工具 临时库存抓取 订单替换

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


    #获取 name异常订单 中的所有订单
    def get_order_all(self,abn_name):
        URL="https://www.erp321.com/app/order/order/list.aspx?ts___=1668157949739&am___=LoadDataToJSON"
        HEADERS={
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.erp321.com',
            'referer': 'https://www.erp321.com/app/order/order/list.aspx',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        VIEWSTATE=quote_plus(self.get_viewstate(url=URL))
        DATA=f"__VIEWSTATE={VIEWSTATE}&__VIEWSTATEGENERATOR=C8154B07&insurePrice=&_jt_page_count_enabled=&_jt_page_increament_enabled=true&_jt_page_increament_page_mode=&_jt_page_increament_key_value=&_jt_page_increament_business_values=&_jt_page_increament_key_name=o_id&_jt_page_size=2000&fe_node_desc=&receiver_state=&receiver_city=&receiver_district=&receiver_address=&receiver_name=&receiver_phone=&receiver_mobile=&check_name=&check_address=&fe_remark_type=single&node_type=&fe_flag=&fe_is_append_remark=&__CALLBACKID=JTable1&__CALLBACKPARAM=%7B%22Method%22%3A%22LoadDataToJSON%22%2C%22Args%22%3A%5B%221%22%2C%22%5B%7B%5C%22k%5C%22%3A%5C%22status%5C%22%2C%5C%22v%5C%22%3A%5C%22question%5C%22%2C%5C%22c%5C%22%3A%5C%22%40%3D%5C%22%7D%2C%7B%5C%22k%5C%22%3A%5C%22question_type%5C%22%2C%5C%22v%5C%22%3A%5C%22{quote_plus(abn_name)}%5C%22%2C%5C%22c%5C%22%3A%5C%22%40%3D%5C%22%7D%5D%22%2C%22%7B%7D%22%5D%7D"
        response=self.requests.post(url=URL,headers=HEADERS,data=DATA)
        rs_value=json.loads(json.loads(response.text[2:])['ReturnValue'])
        DataCount=rs_value['dp']['DataCount']
        Data=rs_value['datas']
        return {'datacount':DataCount,'data':Data}

    #订单替换 商品编码
    def change_code(self,CALLBACKPARAM):
        CALLBACKPARAM['Args'][1]=json.dumps(CALLBACKPARAM['Args'][1])
        CALLBACKPARAM=json.dumps(CALLBACKPARAM)
        # print(CALLBACKPARAM)
        URL="https://ww.erp321.com/app/order/order/list.aspx?ts___=1668492617750&am___=ChangeBatchItem"
        HEADERS={
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://ww.erp321.com',
            'referer': 'https://ww.erp321.com/app/order/order/list.aspx',
            'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42',
            'x-requested-with': 'XMLHttpRequest',
        }
        VIEWSTATE=self.get_viewstate(url=URL)
        DATA={
            "__VIEWSTATE":VIEWSTATE,
            "__VIEWSTATEGENERATOR":"C8154B07",
            "insurePrice":'',
            "_jt_page_count_enabled":'',
            "_jt_page_increament_enabled":True,
            "_jt_page_increament_page_mode":'',
            "_jt_page_increament_key_value":'',
            "_jt_page_increament_business_values":'',
            "_jt_page_increament_key_name":'o_id',
            "_jt_page_size":2000,
            "fe_node_desc":'',
            "receiver_state":'',
            "receiver_city":'',
            "receiver_district":'',
            "receiver_address":'',
            "receiver_name":'',
            "receiver_phone":'',
            "receiver_mobile":'',
            "check_name":'',
            "check_address":'',
            "fe_remark_type":'single',
            "node_type":'',
            "fe_flag":'',
            "fe_is_append_remark":'',
            "__CALLBACKID":'JTable1',
            "__CALLBACKPARAM":CALLBACKPARAM,
        }
        response=self.requests.post(url=URL,headers=HEADERS,data=DATA)
        # print(response.text)
        return json.loads(response.text[2:])

    #通过内部订单号查找当前订单下的商品可用库存
    def get_can_stock(self,o_id):
        oid=int(o_id)
        URL="https://www.erp321.com/app/order/order/list.aspx?ts___=1668668604091&am___=LoadOrderPickable"
        HEADERS={
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.erp321.com',
            'referer': 'https://www.erp321.com/app/order/order/list.aspx',
            'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42',
            'x-requested-with': 'XMLHttpRequest',
        }
        VIEWSTATE=quote_plus(self.get_viewstate(url=URL))
        DATA=f"__VIEWSTATE={VIEWSTATE}&__VIEWSTATEGENERATOR=C8154B07&insurePrice=&_jt_page_count_enabled=&_jt_page_increament_enabled=true&_jt_page_increament_page_mode=&_jt_page_increament_key_value=&_jt_page_increament_business_values=&_jt_page_increament_key_name=o_id&_jt_page_size=2000&fe_node_desc=&receiver_state=&receiver_city=&receiver_district=&receiver_address=&receiver_name=&receiver_phone=&receiver_mobile=&check_name=&check_address=&fe_remark_type=single&node_type=&fe_flag=&fe_is_append_remark=&__CALLBACKID=JTable1&__CALLBACKPARAM=%7B%22Method%22%3A%22LoadOrderPickable%22%2C%22Args%22%3A%5B{oid}%5D%2C%22CallControl%22%3A%22%7Bpage%7D%22%7D"
        response=self.requests.post(url=URL,headers=HEADERS,data=DATA)
        rs_status = json.loads(response.text[2:])['IsSuccess']
        if rs_status:
            return_dict={}
            rs_value = json.loads(response.text[2:])['ReturnValue']
            for k,y in rs_value.items():
                return_dict[y['Skuid']]=y['Pickable']
            return {"status":200,"data":return_dict}
        else:
            return {"status":98,"msg":f"{o_id}查询可用库存失败",'data':{}}

    #抓取PDD店铺当天多维度数据
    def get_dwd_spshop(self,date):
        URL="https://pf.erp321.com/app/FMS/profitfordate/profit.aspx?type=more&timetype=&isads=true&ts___=1669082282343&am___=SetSearchConditionToCacheForFMS"#新版ADS
        # URL="https://pf.erp321.com/app/FMS/profitfordate/profit.aspx?type=more&timetype=&isads=false&ts___=1669082352839&am___=SetSearchConditionToCacheForFMS"#旧版ADS
        HEADERS={
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://pf.erp321.com',
            'referer': 'https://pf.erp321.com/app/FMS/profitfordate/profit.aspx?type=more&timetype=&isads=true',
            'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52',
            'x-requested-with': 'XMLHttpRequest',
        }
        VIEWSTATE=quote_plus(self.get_viewstate(url=URL))
        DATA=f"__VIEWSTATE={VIEWSTATE}&__VIEWSTATEGENERATOR=01C5DAED&__CALLBACKID=ACall1&__CALLBACKPARAM=%7B%22Method%22%3A%22SetSearchConditionToCacheForFMS%22%2C%22Args%22%3A%5B%22%7B%5C%22timetype%5C%22%3A%5C%22%5C%22%2C%5C%22rule_id%5C%22%3A%5C%22331%5C%22%2C%5C%22rule_name%5C%22%3A%5C%22rule_name%5C%22%2C%5C%22datetype%5C%22%3A%5C%22paydate%5C%22%2C%5C%22begin_date%5C%22%3A%5C%22{date}%5C%22%2C%5C%22end_date%5C%22%3A%5C%22{date}%5C%22%2C%5C%22begin_month%5C%22%3A%5C%22%5C%22%2C%5C%22end_month%5C%22%3A%5C%22%5C%22%2C%5C%22shopids%5C%22%3A%5C%2210341596%2C11262554%2C11288284%2C11288291%2C11294381%2C11294678%2C11307275%2C11334060%2C11334176%2C11344631%2C11399960%2C11400108%2C11435776%2C11502800%2C11681580%2C11695590%2C11700009%2C11715876%2C11725757%2C11733025%2C12151690%2C12292666%2C12391281%2C12673200%2C12859321%2C12948336%2C12969045%2C12969130%2C13077664%2C13116222%2C13168313%2C13168328%2C13185372%2C13445299%2C13523091%2C13530518%5C%22%2C%5C%22shopnames%5C%22%3A%5C%22PDD%E7%94%B7%E8%A3%85-ESSECITY%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E7%AB%A5%E8%A3%85-%E5%8F%B2%E5%8A%AA%E6%AF%94%E7%82%AB%E6%B4%BE%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E5%8F%AE%E5%BD%93%E5%88%B6%E9%80%A0%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E7%AB%A5%E8%A3%85-%E5%A9%B4%E9%BA%A6%E5%A5%87%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-I'M%20DAVID%E5%B0%8F%E5%B8%83%E5%AE%B6%2CPDD%E7%AB%A5%E8%A3%85-%E7%94%B0%E8%8A%BD%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E7%AB%A5%E8%A3%85-%E6%8B%89%E5%A4%8F%E8%B4%9D%E5%B0%94%E6%A0%BC%E4%BB%95%E6%B4%9B%2CPDD%E7%AB%A5%E8%A3%85-%E5%B8%83%E6%9C%97%E7%86%8A%E5%A2%9E%E6%98%A5%2CPDD%E7%AB%A5%E8%A3%85-%E6%8B%89%E5%A4%8F%E8%B4%9D%E5%B0%94%E4%BD%91%E9%9D%92%E7%BE%8E%2CPDD%E7%AB%A5%E8%A3%85-%E5%B8%83%E6%9C%97%E7%86%8A%E9%98%85%E9%A6%99%E6%97%B6%E4%BB%A3%2CPDD%E5%A5%B3%E8%A3%85-%E9%AB%98%E6%A2%B5%E6%9D%B0%E4%BC%8A%E6%96%AF%E5%BA%97%2CPDD%E7%AB%A5%E8%A3%85-%E9%AB%98%E6%A2%B5%E9%BA%A6%E5%A8%81%E4%BC%A6%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-%E9%AB%98%E6%A2%B5%E9%94%90%E8%BF%88%E9%91%AB%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-I'MDAVID%E7%A6%BE%E5%AD%A3%E7%BA%AF%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-IM%20DAVID%E4%BC%98%E6%98%8C%E6%BA%90%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-%E9%9B%AA%E4%B8%AD%E9%A3%9E%E8%81%9A%E6%B2%99%E6%88%90%E5%A1%94%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E9%9B%AA%E4%B8%AD%E9%A3%9E%E9%A3%98%E6%80%9D%E8%8A%AC%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-%E9%AB%98%E6%A2%B5%E7%A6%BE%E5%AD%A3%E7%BA%AF%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E9%9B%AA%E4%B8%AD%E9%A3%9E%E9%98%85%E9%A6%99%E6%97%B6%E4%BB%A3%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%AB%A5%E8%A3%85-%E9%9B%AA%E4%B8%AD%E9%A3%9E%E7%A6%BE%E5%AD%A3%E7%BA%AF%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E9%BB%91%E7%99%BD%E7%94%BA%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E4%B9%85%E5%81%9A%E8%8C%83%E5%84%BF%E5%A5%B3%E8%A3%85%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E8%AF%AD%E9%9C%96%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-IM%20DAVID%E8%BE%83%E7%9C%9F%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%AB%A5%E8%A3%85-%E9%9B%AA%E4%B8%AD%E9%A3%9E%E8%B4%9D%E7%8E%B2%E8%8A%AC%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-IM%20DAVID%E5%96%B5%E6%80%9D%E8%8C%83%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-IM%20DAVID%E6%98%9F%E6%9C%AB%E5%BF%B5%E5%A6%A4%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-IM%20DAVID%E8%81%9A%E6%B2%99%E6%88%90%E5%A1%94%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-%E5%B8%83%E8%A1%A3%E4%B8%8D%E4%BA%8C%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-JEANSWEST%E7%9C%9F%E7%BB%B4%E6%96%AF%E4%BC%91%E9%97%B2%E8%A3%85%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E7%9C%9F%E7%BB%B4%E6%96%AF%E8%BE%83%E7%9C%9F%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E7%9C%9F%E7%BB%B4%E6%96%AF%E9%98%85%E9%A6%99%E6%97%B6%E4%BB%A3%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E8%8E%AB%E5%A6%AE%E5%B8%8C%E6%97%97%E8%88%B0%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E7%8E%A9%E6%9C%AA%E9%94%90%E8%B6%8A%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E7%94%B7%E8%A3%85-CK%E7%82%AB%E6%B4%BE%E4%B8%93%E5%8D%96%E5%BA%97%2CPDD%E5%A5%B3%E8%A3%85-%E8%93%9D%E5%8D%93%E6%81%A9%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%5C%22%2C%5C%22customizetype%5C%22%3A%5C%22%5C%22%2C%5C%22customizetypename%5C%22%3A%5C%22%5C%22%2C%5C%22iscustomizetypefindson%5C%22%3Atrue%2C%5C%22returntype%5C%22%3A%5C%22comfirmdate%5C%22%2C%5C%22splitcombine%5C%22%3Atrue%2C%5C%22afsalebeforunexists%5C%22%3Afalse%2C%5C%22isckreturnrecdatesendrtmoney%5C%22%3Afalse%2C%5C%22emdays%5C%22%3A%5C%2215%5C%22%2C%5C%22isflowconfirm%5C%22%3Afalse%2C%5C%22multipleprice%5C%22%3A%5C%220%5C%22%7D%22%5D%2C%22CallControl%22%3A%22%7Bpage%7D%22%7D"
        try:
            response=self.requests.post(url=URL,headers=HEADERS,data=DATA)
            if response.status_code!=200:
                return {"status":False,"msg":"数据抓取出错"}
            re_value=json.loads(response.text[2:])['ReturnValue']
            res2=self.requests.get(url=f"https://pf.erp321.com/app/FMS/profitfordate/profit.aspx?type=more&timetype=&isads=true&export=true&exporttype=spshop&s={re_value}")
            if res2.status_code!=200:
                return {"status":False,"msg":"数据抓取完成,下载失败"}
            cur_day_path=os.path.join(settings.MEDIA_ROOT,f'PDD_dwd_files/汇总表-按店铺拆分_{date}.xlsx')
            with open(cur_day_path,"wb") as f:
                f.write(res2.content)
            return {"status":True,"msg":cur_day_path}
        except Exception as e:
            logging.getLogger('err_log').error(f"日期:{date} 生成多维度数据失败! 原因:{e}")
            return {"status":False,"msg":f"生成多维度数据失败! 原因:{e}"}

    def get_viewstate(self,url):
        res = self.requests.get(url, headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        })
        # print(res.text)
        etree_xpath = etree.HTML(res.text)
        views_date = etree_xpath.xpath("//*[@id='__VIEWSTATE']/@value")[0]
        return views_date
#
# e=erp_stock(cookies="_ati=6352630638178; j_d_3=4LKDCZ5CR7SV4HITD7BCDYZJEB57UKRIAM6PAJB6NW35MD6CJLEYJFZNXNYFETUN5BBHLMVZONL6KAXXMRYGFAGAUE; u_lid=17671611495; 3AB9D23F7A4B3C9B=4LKDCZ5CR7SV4HITD7BCDYZJEB57UKRIAM6PAJB6NW35MD6CJLEYJFZNXNYFETUN5BBHLMVZONL6KAXXMRYGFAGAUE; u_name=%e4%be%af%e6%96%87%e6%9d%b0; u_ssi=; u_co_name=%e6%ad%a6%e6%b1%89%e5%b0%8f%e5%b8%83%e7%94%b5%e5%ad%90%e5%95%86%e5%8a%a1%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8; u_drp=-1; v_d_144=1668314796715_f98c64ebd87b2f429a9431ca973043a3; u_cid=133127884618026377; u_r=12%2c13%2c14%2c15%2c17%2c18%2c22%2c23%2c27%2c28%2c29%2c30%2c31%2c32%2c33%2c34%2c35%2c36%2c39%2c40%2c41%2c52%2c53%2c54%2c61%2c62%2c101; u_sso_token=CS@2d51df25a7214b1693656f7642d95878; u_id=14168375; u_shop=-1; u_co_id=10174711; p_50=26C928C6EF9A39D40E0E4041E05F0C40638039404618035306%7c10174711; u_env_next=www; u_env=www; u_json=%7b%22t%22%3a%222022-11-21+11%3a40%3a56%22%2c%22co_type%22%3a%22%e6%a0%87%e5%87%86%e5%95%86%e5%ae%b6%22%2c%22proxy%22%3anull%2c%22ug_id%22%3a%2211003725%22%2c%22dbc%22%3a%221149%22%2c%22tt%22%3a%2295%22%2c%22apps%22%3a%221.4.7.150.152%22%2c%22pwd_valid%22%3a%220%22%2c%22ssi%22%3a%22%22%2c%22sign%22%3a%223463957.4FA09C87875C434C82CF461C38CFFCC7%2c83ced691def5811a59f5a93e6a7e6750%22%7d; acw_tc=2760779716690801989404444e2d86c92321b30ef570f847e8a1bd332cf539")
# e.get_dwd_spshop(date="2022-11-19")
#
#
