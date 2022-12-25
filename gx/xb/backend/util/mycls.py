import threading


class MyResponse:
    def __init__(self):
        self.status=7000
        self.msg='未响应返回值'
        self.data={}

    @property
    def get_dict(self):
        return self.__dict__

    #成功返回值
    def is_ok(self,data):
        self.status=200
        self.msg="成功"
        self.data=data

    #成功返回值_带count
    def is_ok_count(self,data,count):
        self.status=200
        self.msg="成功"
        self.count=count
        self.data=data

    #修改所有
    def change(self,status,msg,data):
        self.status=status
        self.msg=msg
        self.data=data

    #校验错误返回值
    def check_err(self,data_errors):
        self.status = 99
        self.msg = "数据校验错误"+str(data_errors)
        self.data=data_errors

    #查询数据为控
    def none_err(self):
        self.status=97
        self.msg="操作数据为空"
        self.data={}

    #缺少接口参数
    def need_parameter_err(self):
        self.status = 96
        self.msg = "缺少接口参数"
        self.data = {}

    #请先登陆再进行操作
    def session_err(self):
        self.status=-1
        self.msg="请先登陆"
        self.data={}

class Myfunction:
    def __init__(self,serializer):
        self.serializer=serializer

    # 单个新增
    def obj_add(self,rs_data):
        obj_ser = self.serializer(data=rs_data)  # 序列化对象
        # 序列化校验
        if not obj_ser.is_valid():
            return {'status': 99, 'data': {}, 'msg': f'数据校验错误--{obj_ser.errors}'}
        else:
            obj_ser.save()  # 成功则保存
            return {'status': 200, 'data': obj_ser.data, 'msg': '增加成功'}


