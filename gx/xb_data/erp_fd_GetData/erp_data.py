
import time
from lxml import etree
import requests,json
from urllib.parse import quote_plus
from threading import Thread

from erp_fd_GetData.erpStock_exts import *
from exts import *

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

    #获取金桥仓库 成品装库存
    def get_male_stock(self):
        self.male_stock_data=[]
        #获取总页数 总数据条数
        one_data=self.__male_stock_one(val_type=False)
        PageCount=one_data['PageCount']
        DataCount=one_data['DataCount']
        print("########抓取金桥仓 成品装###########")
        print(f"总页数:  {PageCount}")
        print(f"数据总条数:  {DataCount}")
        #开多线程抓取数据
        index=0
        while True:
            cur_task=[]
            for i in range(5):
                index+=1
                print("当前抓取第 {} 页".format(index))
                t=Thread(target=self.__male_stock_one,args=(index,))
                cur_task.append(t)
                if index >= PageCount:
                    break
            for i in cur_task:
                i.start()
            for i in cur_task:
                i.join()
            #
            if index>=PageCount:
                break
        return self.male_stock_data

    def __male_stock_one(self,index=1,val_type=True):
        viewstate = self.get_viewstate(url=ERP_XJCWKC_VIEWSTATE_URL)
        data = f"__VIEWSTATE={quote_plus(viewstate)}&__VIEWSTATEGENERATOR=2F6CC565&owner_co_id=10174711&authorize_co_id=11529535&i_id=&sku_id=&combine_sku_id=&name=&properties_value=&bin=CP-&pack_id=&io_id=&supplier_id=&supplier_name=&pack_type=&_jt_page_count_enabled=&_jt_page_size=200&__CALLBACKID=JTable1&__CALLBACKPARAM=%7B%22Method%22%3A%22LoadDataToJSON%22%2C%22Args%22%3A%5B%22{index}%22%2C%22%5B%7B%5C%22k%5C%22%3A%5C%22%5Bp%5D.bin%5C%22%2C%5C%22v%5C%22%3A%5C%22CP-%5C%22%2C%5C%22c%5C%22%3A%5C%22rightlike%5C%22%7D%2C%7B%5C%22k%5C%22%3A%5C%22%5Bp%5D.wh_id%5C%22%2C%5C%22v%5C%22%3A%5C%220%5C%22%2C%5C%22c%5C%22%3A%5C%22%3E%5C%22%7D%5D%22%2C%22%7B%7D%22%5D%7D"
        response = self.requests.post(url=ERP_MALE_STOCK_URL, headers=ERP_MALE_STOCK_HEADERS, data=data)
        return_val = json.loads(json.loads(response.text[2:])['ReturnValue'])
        PageCount = return_val['dp']['PageCount']
        DataCount = return_val['dp']['DataCount']

        if val_type:
            self.male_stock_data.extend(return_val["datas"])
        else:
            return {'PageCount':PageCount,'DataCount':DataCount}

    # 获取女装主仓仓库 成品装库存
    def get_female_stock(self):
        self.female_stock_data = []
        # 获取总页数 总数据条数
        one_data = self.__female_stock_one(val_type=False)
        PageCount = one_data['PageCount']
        DataCount = one_data['DataCount']
        print("########抓取女装主仓 成品装###########")
        print(f"总页数:  {PageCount}")
        print(f"数据总条数:  {DataCount}")
        # 开多线程抓取数据
        index = 0
        while True:
            cur_task = []
            for i in range(5):
                index += 1
                print("当前抓取第 {} 页".format(index))
                t = Thread(target=self.__female_stock_one, args=(index,))
                cur_task.append(t)
                if index >= PageCount:
                    break
            for i in cur_task:
                i.start()
            for i in cur_task:
                i.join()
            #
            if index >= PageCount:
                break
        return self.female_stock_data

    def __female_stock_one(self, index=1, val_type=True):
        viewstate = self.get_viewstate(url=ERP_FEMALE_STOCK_URL)
        data = f"__VIEWSTATE={quote_plus(viewstate)}&__VIEWSTATEGENERATOR=2F6CC565&owner_co_id=10174711&authorize_co_id=10174711&i_id=&sku_id=&combine_sku_id=&name=&properties_value=&bin=CP-&pack_id=&io_id=&pack_type=&_jt_page_count_enabled=&_jt_page_size=200&__CALLBACKID=JTable1&__CALLBACKPARAM=%7B%22Method%22%3A%22LoadDataToJSON%22%2C%22Args%22%3A%5B%22{index}%22%2C%22%5B%7B%5C%22k%5C%22%3A%5C%22%5Bp%5D.bin%5C%22%2C%5C%22v%5C%22%3A%5C%22CP-%5C%22%2C%5C%22c%5C%22%3A%5C%22rightlike%5C%22%7D%2C%7B%5C%22k%5C%22%3A%5C%22%5Bp%5D.wh_id%5C%22%2C%5C%22v%5C%22%3A%5C%220%5C%22%2C%5C%22c%5C%22%3A%5C%22%3E%5C%22%7D%5D%22%2C%22%7B%7D%22%5D%7D"
        response = self.requests.post(url=ERP_FEMALE_STOCK_URL, headers=ERP_FEMALE_STOCK_HEADERS, data=data)
        return_val = json.loads(json.loads(response.text[2:])['ReturnValue'])
        PageCount = return_val['dp']['PageCount']
        DataCount = return_val['dp']['DataCount']

        if val_type:
            self.female_stock_data.extend(return_val["datas"])
        else:
            return {'PageCount': PageCount, 'DataCount': DataCount}

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






