from django.urls import path,include,re_path
from rest_framework import routers
from django.views.static import serve


from app.views import *
from app.views.finace import *
from app.views.dy_views import *
from app.views.pdd_views import *
from backend.settings import MEDIA_ROOT
router=routers.SimpleRouter()

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),


    #店铺路由
    path('shop',ShopView.ShopViewSet.as_view()),
    re_path('shop/(?P<id>\d+)',ShopView.ShopViewSetFilter.as_view()),
    path('shop/addmany',ShopView.many_shop_add),#自定义路由

    #自定义路由###################################################
    #dy_survey
    path('dy/survey',dy_SalesView.show_dy_suery),

    #生成vcode发送邮件
    path('us/register/cemail',UsersView.create_vcode),
    # 用户查看邮箱是否被注册
    path('us/register/checkemail', UsersView.check_email),
    #用户登录
    path('login', UsersView.us_login),
    #用户验证session
    path('check/session',UsersView.check_session),
    ############################################################

    #cookie路由
    path('cks',CookiewView.CookiesViewSet.as_view()),#查询所有 新增

    #成本价路由
    path('finace/fcost',Finace_CostView.FinaceCostViewSet.as_view()),
    re_path('finace/fcost/filter',Finace_CostView.FinaceCostViewSetFilter.as_view()),
    path('finace/newfcost',Finace_CostView.import_newCost),

    #吊牌价路由
    path('finace/tags',Finace_TagView.FinaceTagViewSet.as_view()),
    re_path('finace/tag/filter',Finace_TagView.FinaceCostViewSetFilter.as_view()),
    path('finace/newtag',Finace_TagView.import_newTag),

    #抖音财务
    #dy_sales
    path('dy/sales',dy_SalesView.dySalesViewSet.as_view()),
    re_path('dy/sales/(?P<id>\d+)',dy_SalesView.dySalesViewSetFilter.as_view()),#修改推广费用 客服返现
    #dy_sendcost
    path('dy/sendcost',dy_SendCostView.dySendCostViewSet.as_view()),
    #dy_sendgoods
    path('dy/sendgoods',dy_SendGoodsView.dySendGoodsViewSet.as_view()),


    #拼多多财务
    #pdd_shop_names
    path('pdd/shops',pdd_SalesView.get_shop_all),
    #pdd_record
    path('pdd/record',pdd_RecordView.pddRecordViewSet.as_view()),
    #pdd_sales
    path('pdd/sales',pdd_SalesView.pddSalesViewSet.as_view()),
    #pdd_sendcost
    path('pdd/sendcost',pdd_SendCostView.pddSendCostViewSet.as_view()),
    #pdd_sendgoods
    path('pdd/sendgoods',pdd_SendGoodsView.pddSendGoodsViewSet.as_view()),
    #自定义接口 拼多多获取多维度数据
    path('pdd/dwd_data',pdd_SalesView.get_dwd_data),
    #自定义接口 export拼多多
    path('pdd/export', pdd_SalesView.export_pddday),
    #自定义接口 pdd修改3号状态
    path('pdd/upstatus', pdd_SalesView.update_date_status),
    #自定义接口 通过时间查询pdd数据流程情况
    path('pdd/dateStatus', pdd_SalesView.pdd_get_date_status),
    #自定义接口 最终汇总
    path('pdd/generate',pdd_SalesView.generate_data_count),


    #自定义路由

    #用户路由
    path('user',UsersView.UsersViewSet.as_view()),
    re_path('user/(?P<pk>\d+)',UsersView.UsersViewSetFilter.as_view()),
]

urlpatterns+=router.urls