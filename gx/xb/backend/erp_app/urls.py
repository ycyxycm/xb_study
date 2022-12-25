from django.urls import path,include,re_path
from rest_framework import routers
from django.views.static import serve


from erp_app.views import *
router=routers.SimpleRouter()

urlpatterns = [
    #自定义路由###################################################
    path('get_orders',OrderView.get_orders),#获取异常类型所有订单
    path('change_sku',OrderView.change_fd),#福袋替换成品
    path('matching_sku',OrderView.matching_fd),#福袋匹配成品
    path('matching_stock',OrderView.matching_stock),#福袋匹配可用库存
    ############################################################

]

urlpatterns+=router.urls