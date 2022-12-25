from django.db.models import Sum, F

from app import models
from conf.exts import *

class dySales:
    def __init__(self,sales_dict):
        self.id=sales_dict['id']
        self.shop=sales_dict['shop']
        self.now_date = sales_dict['now_date']
        self.deal_price = float(sales_dict['deal_price'])
        self.refund_price = float(sales_dict['refund_price'])
        self.budan_price = float(sales_dict['budan_price'])
        self.budan_yongjin = float(sales_dict['budan_yongjin'])
        self.extension_price = float(sales_dict['extension_price'])
        self.kf_re_price = float(sales_dict['kf_re_price'])

        self.ser_charge=round(float((self.deal_price-self.refund_price)*0.05),2)# 服务费 (成交金额-退款金额)*0.05
        self.freight = float(sales_dict['freight'])
        self.collect_timeout=float(sales_dict['collect_timeout'])
        self.fake_send_timeout = float(sales_dict['fake_send_timeout'])
        self.send_timeout = float(sales_dict['send_timeout'])
        self.small_pay = float(sales_dict['small_pay'])
        self.violation = float(sales_dict['violation'])
        self.daren_yongjin = float(sales_dict['daren_yongjin'])
        self.marketing = float(sales_dict['marketing'])


    @property
    def get_dict(self):
        return self.__dict__

    #其他数据的计算及返回
    def new_date(self):
        send_number = models.dy_sendgoods.objects.filter(shop=self.shop, now_date=self.now_date).first()  # 当前店铺 日期发货时间

        # 退款率=退款金额/(成交金额-补单金额)
        try:
            self.refund_rate="{}%".format(round((self.refund_price/(self.deal_price-self.budan_price))*100,2))
        except ZeroDivisionError:
            self.refund_rate="0.00%"
        #print("1")

        # 吊牌费（实发数量-实退数量）*吊牌费
        if self.shop=="DY童装-拉夏聚沙成塔店":
            self.label_price=round(count_label(self.shop,self.now_date),2)
        else:
            self.label_price=0
        #print("2")

        # 净销售额=成交金额-退款金额-补单金额
        self.net_sales=round(self.deal_price-self.refund_price-self.budan_price,2)
        # print("3")

        # 平台花费=服务费+运费险+发货超时+揽收超时+虚假发货超时+小额打款+违规+达人带货佣金+营销费用划扣
        self.plat_cost=round(self.ser_charge+self.freight+self.send_timeout+self.collect_timeout+self.fake_send_timeout+self.small_pay+self.violation+self.daren_yongjin+self.marketing,2)
        #print("4")

        # 销售毛利率=(净销售额-推广费用-补单佣金-平台花费-客服返现)/净销售额
        try:
            self.gpmo_sales="{}%".format(
                round(((self.net_sales-self.extension_price-self.budan_yongjin-self.plat_cost-self.kf_re_price)
                      /self.net_sales)*100,2)
            )
        except ZeroDivisionError:
            self.gpmo_sales="0.00%"
        #print("5")

        #获取当前当铺当天补单发货数量
        cur_budan_send_number = models.dy_sendcost.objects.filter(shop=self.shop, now_date=self.now_date,
                                                                   stylecode="补单发货编码").first()
        if cur_budan_send_number is None:
            self.budan_send_number = 0
        else:
            self.budan_send_number = cur_budan_send_number.send_number

        # 快递费用=(当前店铺的发货数量-补单发货数量)*2.7
        if send_number is None:
            self.express_price=round(0,2)
        else:
            self.express_price=round(((send_number.order_number-self.budan_send_number)*2.7),2)
        #print("6")

        # 发货费用=(当前店铺的发货数量-补单发货数量)*2
        if send_number is None:
            self.deliver_price=round(0,2)
        else:
            self.deliver_price=round(((send_number.order_number-self.budan_send_number)*2),2)
        # print("7")

        # 补单快递费
        self.budan_express_price = round(self.budan_send_number * 2.4, 2)

        # 补单发货费
        self.budan_deliver_price = round(self.budan_send_number * 0.2, 2)

        # 衣服成本=当前店铺的成本价总和-发货后退款成本*0.6 old
        # 衣服成本=当前店铺的成本价总和-发货后退款成本*0.75 new
        cur_cbj_count=models.dy_sendcost.objects.filter(shop=self.shop,now_date=self.now_date).aggregate(
            cbj_cSum=Sum(F("send_number") * F("today_price")))['cbj_cSum']
        self.cbj_count = 0 if cur_cbj_count is None else float(cur_cbj_count)
        if send_number is None:
            cur_float=0.00
        else:
            cur_float=float(send_number.send_refund_cost) * 0.75
        self.cbj_count = round(float(self.cbj_count) - cur_float, 2)


        # print("8")

        # 毛利率=(净销售额-衣服成本-发货费用-快递费用-吊牌费-补单发货费用-补单快递费用)/净销售额
        try:
            self.gpm="{}%".format(round(((self.net_sales-self.cbj_count-self.deliver_price-self.express_price-
                                          self.label_price-self.budan_deliver_price-self.budan_express_price)/self.net_sales)*100,2))
        except ZeroDivisionError:
            self.gpm="0.00%"
        # print("9")

        # 利润预估=净销售额-补单佣金-推广费用-平台花费-吊牌费-衣服成本-客服返现-快递费用-发货费用-补单发货费用-补单快递费用
        self.profit_es=round(self.net_sales-self.budan_yongjin-self.extension_price-self.plat_cost-self.label_price-
                             self.cbj_count-self.kf_re_price-self.express_price-self.deliver_price
                             -self.budan_deliver_price-self.budan_express_price,2)
        # print("10")

        # 净毛利率=利润预估/净销售额
        try:
            self.jmll="{}%".format(round((self.profit_es/self.net_sales)*100,2))
        except ZeroDivisionError:
            self.jmll="0.00%"
        # print("11")

        # print("ok")
#抖音概况
class dySurvey:
    def __init__(self, shop,start_date,end_date):
        # self.now_date=now_date_dict#{"start_date":2022-01-01,"end_date":2022-01-30}

        self.start_date=start_date
        self.end_date=end_date

        self.shop=shop
        # 净销售额合计
        self.net_sales_sum = 0
        # 利润预估合计
        self.profit_es_sum = 0

        #本月利润预估
        self.profit_es_s=[]
        obj_all=models.dy_sales.objects.filter(shop=shop,now_date__gte=self.start_date,now_date__lte=self.end_date).all()
        for i in obj_all:
            ds=dySales(i.__dict__)
            ds.new_date()
            self.profit_es_s.append({'su_nowdate':ds.now_date,'su_profit':ds.profit_es,'su_net_sales':ds.net_sales})
            self.net_sales_sum+=round(ds.net_sales,2)
            self.profit_es_sum+=round(ds.profit_es,2)

        # 净销售额合计
        self.net_sales_sum = round(self.net_sales_sum,2)
        # 利润预估合计
        self.profit_es_sum = round(self.profit_es_sum,2)

        # 净毛利率
        try:
            self.jmll_sum=f"{round((self.profit_es_sum/self.net_sales_sum)*100,2)}%"
        except ZeroDivisionError as e:
            self.jmll_sum=f"0.00%"

    @property
    def get_dict(self):
        return self.__dict__

# 计算吊牌价 吊牌费是（销售数量-实退数量）*吊牌单价
def count_label(shop_name, time):
    current = models.dy_sendcost.objects.filter(shop=shop_name, now_date=time).all()
    count_price = 0
    for i in current:
        tag_obj = models.finace_tag_price.objects.filter(shop=shop_name).first()
        if get_now_sex(i.stylecode)==0:
            current_label_pirce = tag_obj.female_tag  # 女装吊牌价
        elif get_now_sex(i.stylecode)==2:
            current_label_pirce = tag_obj.child_tag  # 童装吊牌价
        else:
            # print(f"{shop_name}--{i.stylecode}-{time}  吊牌价ERROR 款式列表之外的款式")
            current_label_pirce = 0
        count_price += round((int(i.send_number)-int(i.refund_number)) * float(current_label_pirce), 2)
    return count_price