from django.db.models import Sum, F

from app import models
from conf.exts import *
class pdd_tb1:
    def __init__(self,sales_dict):
        self.shop = sales_dict['shop']
        self.now_date = sales_dict['now_date']
        self.deal_price = float(sales_dict['deal_price'])
        self.refund_price = float(sales_dict['refund_price'])
        self.dd_scene = float(sales_dict['dd_scene'])
        self.dd_search = float(sales_dict['dd_search'])
        self.fxt = float(sales_dict['fxt'])
        self.qztg = float(sales_dict['qztg'])
        self.budan_price = float(sales_dict['budan_price'])
        self.budan_yongjin = float(sales_dict['budan_yongjin'])

    @property
    def get_dict(self):
        return self.__dict__

    def new_data(self):
        tag_obj=models.finace_tag_price.objects.filter(shop=self.shop).first()
        if tag_obj !=None:
            #当天吊牌单价-男
            self.today_male_tag=tag_obj.male_tag
            # print("1")

            #当天吊牌单价-女
            self.today_female_tag=tag_obj.female_tag
            # print("1")

            #当天吊牌单价-童
            self.today_child_tag=tag_obj.child_tag
            # print("1")
        else:
            self.today_male_tag = "此店铺未录入吊牌价"

            self.today_female_tag = "此店铺未录入吊牌价"

            self.today_child_tag = "此店铺未录入吊牌价"

        #销售数量(所有款式总和)
        shop_number_sum=models.pdd_sendcost.objects.filter(shop=self.shop,now_date=self.now_date).aggregate(Sum('send_number'))
        if shop_number_sum['send_number__sum'] is None:
            self.shop_number=0
        else:
            self.shop_number=shop_number_sum['send_number__sum']
        #print("1")

        #实退数量
        refund_number_sum=models.pdd_sendcost.objects.filter(shop=self.shop,now_date=self.now_date).aggregate(Sum('refund_number'))
        if refund_number_sum['refund_number__sum'] is None:
            self.refund_number= 0
        else:
            self.refund_number=refund_number_sum['refund_number__sum']
        #成本汇总(款式销量*款式成本 所有款式总和)
        cur_cost_count=models.pdd_sendcost.objects.filter(shop=self.shop, now_date=self.now_date).aggregate(
            cost_count=Sum(F("send_number")*F("today_price")))['cost_count']
        self.cost_count=0 if cur_cost_count is None else float(cur_cost_count)
        # 吊牌费(男女童款式销量*款式成本价 所有款式总和)
        cur_tag_count=models.pdd_sendcost.objects.filter(shop=self.shop, now_date=self.now_date).aggregate(
            tag_count=Sum(F("send_number") * F("today_tag")))['tag_count']
        self.tag_count=0 if cur_tag_count is None else float(cur_tag_count)
        # 吊牌返还费
        cur_refund_tag_count=models.pdd_sendcost.objects.filter(shop=self.shop, now_date=self.now_date).aggregate(
            rtag_count=Sum(F("refund_number") * F("today_tag")))['rtag_count']
        self.refund_tag_count=0 if cur_refund_tag_count is None else float(cur_refund_tag_count)

        #特殊店铺吊牌价
        try:
            # 成交金额-退款金额-补单金额*品牌价
            if self.shop=="PDD男装-JEANSWEST真维斯休闲装旗舰店":
                self.tag_count+=(self.deal_price-self.refund_price-self.budan_price)*0.072
            if self.shop=="PDD女装-真维斯较真专卖店":
                self.tag_count+=(self.deal_price-self.refund_price-self.budan_price)*0.072
            if self.shop=="PDD女装-真维斯阅香时代专卖店":
                self.tag_count+=(self.deal_price-self.refund_price-self.budan_price)*0.072
        except Exception as e:
            print(e)

        #原始线上订单数量(当天发货数)
        sendgoods_obj=models.pdd_sendgoods.objects.filter(shop=self.shop, now_date=self.now_date).first()
        if sendgoods_obj is None:
            or_number=0
        else:
            or_number = sendgoods_obj.order_number
        self.sendgoods_number=or_number

        #获取当前当铺当天补单发货数量
        cur_budan_send_number=models.pdd_sendcost.objects.filter(shop=self.shop,now_date=self.now_date,stylecode="补单发货编码").first()
        if cur_budan_send_number is None:
            self.budan_send_number=0
        else:
            self.budan_send_number=cur_budan_send_number.send_number

        #快递费(当天发货数*2.7)
        self.express_price = round((self.sendgoods_number-self.budan_send_number)*2.7,2)
        #补单快递费
        self.budan_express_price=round(self.budan_send_number*2.4,2)

        #发货费(当天发货数*2)
        self.deliver_price = round((self.sendgoods_number-self.budan_send_number)*2,2)
        #补单发货费
        self.budan_deliver_price =round(self.budan_send_number*0.2,2)

        #四舍五入保留两位小数
        self.cost_count = round(self.cost_count,2)
        self.tag_count = round(self.tag_count, 2)
        self.refund_tag_count = round(self.refund_tag_count, 2)

    def new2_data(self):
        cur_obj = models.pdd_day_record.objects.filter(shop=self.shop, now_date=self.now_date).all()
        # print(cur_obj)
        # cur_dict={}
        # for i in cur_obj:
        #     cur_dict[i.name]=float(i.price)

        cur_dict={i.name:float(i.price) for i in cur_obj}

        # 全站推广=DWD全站推广
        self.i_qztg=0 if "全站推广" not in cur_dict else cur_dict['全站推广']

        # 售后费用=DWD售后费用
        self.i_sale_after_fee = 0 if "售后费用" not in cur_dict else cur_dict['售后费用']

        # 1.1退货件成本=DWD发货后退款成本*0.75   11-22号0.6改为0.75
        self.i_return_goods_cost_11 = 0 if "发货后退款成本" not in cur_dict else cur_dict['发货后退款成本']*0.75

        # 发货后退款金额=DWD发货后退款额
        self.i_sendgoods_after_refund_money= 0 if "发货后退款额" not in cur_dict else cur_dict['发货后退款额']

        # 发货前退款金额=DWD发货前退款额
        self.i_sendgoods_front_refund_money = 0 if "发货前退款额" not in cur_dict else cur_dict['发货前退款额']

        # 运费险=DWD退货包运费
        self.i_freight=0 if "退货包运费" not in cur_dict else cur_dict['退货包运费']

        # 纸巾=DWD纸巾
        self.i_tissue=0 if "纸巾" not in cur_dict else cur_dict['纸巾']

        # 百亿补贴=DWD百亿补贴活动服务费
        self.i_bybt=0 if "百亿补贴活动服务费" not in cur_dict else cur_dict['百亿补贴活动服务费']

        # 补单佣金=DWD特殊单佣金
        self.i_budan_comm=0 if "特殊单佣金" not in cur_dict else cur_dict['特殊单佣金']

        # 成交金额=DWD付款订单金额
        self.i_deal_money=0 if "付款订单金额" not in cur_dict else round(cur_dict['付款订单金额'],2)

        # 吊牌返还=DWD吊牌返还
        self.i_tag_return=0 if "吊牌返还" not in cur_dict else cur_dict['吊牌返还']

        # 快递超时罚款=DWD快递超时罚款
        self.i_express_overtime=0 if "快递超时罚款" not in cur_dict else cur_dict['快递超时罚款']

        # 短信费=DWD发货短信提醒
        self.i_sms_fee=0 if "发货短信提醒" not in cur_dict else cur_dict['发货短信提醒']

        # 多多进宝=DWD推广及宣传-其他
        self.i_dd_jinbao=0 if "推广及宣传-其他" not in cur_dict else cur_dict['推广及宣传-其他']

        # 多多搜索和场景=DWD多多搜索+多多推广
        self.i_dd_search_scene=0 if "多多搜索+多多推广" not in cur_dict else cur_dict['多多搜索+多多推广']

        # 发货后退款成本=DWD发货后退款成本
        self.i_sendgoods_after_cost=0 if "发货后退款成本" not in cur_dict else cur_dict['发货后退款成本']

        # 放心推=DWD放心推
        self.i_fxt=0 if "放心推" not in cur_dict else cur_dict['放心推']

        # 货款充值跨店满减=DWD货款充值跨店满减
        self.i_loan=0 if "货款充值跨店满减" not in cur_dict else cur_dict['货款充值跨店满减']

        # 客服返现=DWD客服返现
        self.i_kffx=0 if "客服返现" not in cur_dict else cur_dict['客服返现']

        # 拼多多技术服务费=DWD拼多多技术服务费
        self.i_pdd_tech_money=0 if "拼多多技术服务费" not in cur_dict else cur_dict['拼多多技术服务费']

        # 发货费用=DWD发货费用+DWD补单发货费用
        cur_number_fh1=0 if "发货费用" not in cur_dict else cur_dict['发货费用']
        cur_number_bd1=0 if "补单发货费用" not in cur_dict else cur_dict['补单发货费用']
        self.i_sendgoods_fee= cur_number_fh1+ cur_number_bd1

        # 补单金额=DWD分类单付款金额-DWD分类单发货前退款额-DWD分类单发货后退款额
        cur_number_001=0 if "分类单付款金额" not in cur_dict else cur_dict['分类单付款金额']
        cur_number_002=0 if "分类单发货前退款额" not in cur_dict else cur_dict['分类单发货前退款额']
        cur_number_003=0 if "分类单发货后退款额" not in cur_dict else cur_dict['分类单发货后退款额']
        self.i_budan_money=cur_number_001-cur_number_002-cur_number_003

        # 退款金额=[发货前退款额]+[发货后退款额]
        self.i_refund_money = round(self.i_sendgoods_front_refund_money + self.i_sendgoods_after_refund_money,2)

        # 吊牌费=DWD产品包装耗材-[吊牌返还]
        cur_number_004=0 if "产品包装耗材" not in cur_dict else cur_dict['产品包装耗材']
        self.i_tag_fee=cur_number_004-self.i_tag_return

        # 付费推广合计 = [多多搜索和场景]+[补单佣金]+[放心推]+[多多进宝]+[全站推广]
        self.i_tg_pay_count=round(self.i_dd_search_scene+self.i_budan_comm+self.i_fxt+self.i_dd_jinbao+self.i_qztg,2)

        # 活动费用 = [百亿补贴]+[货款充值跨店满减]
        self.i_huodong_fee=round(self.i_bybt+self.i_loan,2)

        # 净销售额 = ROUND([成交金额]-[退款金额]-[补单金额],2)
        self.i_net_sale=round(self.i_deal_money-self.i_refund_money-self.i_budan_money,2)

        # 客服费用合计 = [客服返现]+[售后费用]
        self.i_kf_fee_count=round(self.i_kffx+self.i_sale_after_fee,2)

        # 快递费用=DWD发货及快递费用+[纸巾]+DWD特殊单+DWD快递费用+DWD补单快递费用
        cur_num1=0 if "发货及快递费用" not in cur_dict else cur_dict['发货及快递费用']
        cur_num2 =0 if "特殊单" not in cur_dict else cur_dict['特殊单']
        cur_num3 =0 if "快递费用" not in cur_dict else cur_dict['快递费用']
        cur_num4 =0 if "补单快递费用" not in cur_dict else cur_dict['补单快递费用']
        self.i_kuaidi_fee=cur_num1+self.i_tissue+cur_num2+cur_num3+cur_num4

        # 平台扣费合计 = [运费险]+[拼多多技术服务费]+[快递超时罚款]+[短信费]
        self.i_plat_fee_count=round(self.i_freight+self.i_pdd_tech_money+self.i_express_overtime+self.i_sms_fee,2)

        # 1.1衣服成本=DWD销售成本-[退货件成本1.1]
        cur_number_005=0 if "销售成本" not in cur_dict else cur_dict['销售成本']
        self.i_clothing_cost_11=round(cur_number_005-self.i_return_goods_cost_11,2)

        # 1.1毛利 = [净销售额]-[1.1衣服成本]-[快递费用]-[发货费用]
        self.i_ml_11=round(self.i_net_sale-self.i_clothing_cost_11-self.i_kuaidi_fee-self.i_sendgoods_fee,2)

        # 1.1净毛利=[1.1毛利]-[付费推广合计]-[平台扣费合计]-[客服费用合计]-[活动费用]-[吊牌费]
        self.i_net_ml_11=round(self.i_ml_11-self.i_tg_pay_count-self.i_plat_fee_count-self.i_kf_fee_count-self.i_huodong_fee-self.i_tag_fee,2)

        # 1.0衣服成本=1.1衣服成本/1.1
        self.i_clothing_cost_10=round(chufa(self.i_clothing_cost_11,1.1),2)

        # 1.0退货件成本=DWD发货后退款成本/2/1.1
        cur_number_006=0 if "发货后退款成本" not in cur_dict else cur_dict['发货后退款成本']
        self.i_return_goods_cost_10=chufa(cur_number_006,2*1.1)

        # 1.0毛利= [净销售额]-[1.0衣服成本]-[快递费用]-[发货费用]+[退货件成本1.0]
        self.i_ml_10=round(self.i_net_sale-self.i_clothing_cost_10-self.i_kuaidi_fee-self.i_sendgoods_fee+self.i_return_goods_cost_10,2)

        # 1.0净毛利=[1.0毛利]-[付费推广合计]-[平台扣费合计]-[客服费用合计]-[活动费用]-[吊牌费]
        self.i_net_ml_10=round(self.i_ml_10-self.i_tg_pay_count-self.i_plat_fee_count-self.i_kf_fee_count-self.i_huodong_fee-self.i_tag_fee,2)

        '''
            比例
        '''
        #1.0净毛利率=1.0净毛利/净销售额
        self.i_net_ml_rate_10=str(round(chufa(self.i_net_ml_10,self.i_net_sale)*100,2))+"%"

        #1.0衣服成本占比=1.0衣服成本/净销售额
        self.i_clothing_cost_rate_10 = str(round(chufa(self.i_clothing_cost_10, self.i_net_sale)*100,2))+"%"

        #1.1净毛利率=1.1净毛利/净销售额
        self.i_net_ml_rate_11= str(round(chufa(self.i_net_ml_11, self.i_net_sale)*100,2))+"%"

        #1.1衣服成本占比=1.1衣服成本/净销售额
        self.i_clothing_cost_rate_11 = str(round(chufa(self.i_clothing_cost_11, self.i_net_sale)*100,2))+"%"

        #补单率=补单金额/成交金额
        self.i_budan_rate=str(round(chufa(self.i_budan_money,self.i_deal_money)*100,2))+"%"

        #店长利润系数=1.1净毛利率*10
        self.i_dz_lirun=self.i_net_ml_rate_11*10

        #吊牌费用占比=吊牌费/净销售额
        self.i_tag_fee_rate=str(round(chufa(self.i_tag_fee,self.i_net_sale)*100,2))+"%"

        #发货费用占比=快递费用/净销售额
        self.i_sendgoods_fee_rate=str(round(chufa(self.i_sendgoods_fee,self.i_net_sale)*100,2))+"%"

        #发货后退款率=发货后退款金额/（成交金额-补单金额）
        self.i_sendgoods_after_refund_rate=str(round(chufa(self.i_sendgoods_after_refund_money,self.i_deal_money-self.i_budan_money)*100,2))+"%"

        #活动费用占比=活动费用/净销售额
        self.i_huodong_fee_rate=str(round(chufa(self.i_huodong_fee,self.i_net_sale)*100,2))+"%"

        #客服费用占比=客服费用合计/净销售额
        self.i_kf_fee_rate=str(round(chufa(self.i_kf_fee_count,self.i_net_sale)*100,2))+"%"

        #平台扣费占比=平台扣费合计/净销售额
        self.i_plat_fee_rate=str(round(chufa(self.i_plat_fee_count,self.i_net_sale)*100,2))+"%"

        #退货衣服成本占比=退货件成本1.1/净销售额
        self.i_return_goods_cost_rate=str(round(chufa(self.i_return_goods_cost_11,self.i_net_sale)*100,2))+"%"

        #退款率=退款金额/（成交金额-补单金额）
        self.i_refund_rate=str(round(chufa(self.i_refund_money,self.i_deal_money-self.i_budan_money)*100,2))+"%"

        #运营付费占比=付费推广合计/净销售额
        self.i_tg_pat_rate=str(round(chufa(self.i_tg_pay_count,self.i_net_sale)*100,2))+"%"

