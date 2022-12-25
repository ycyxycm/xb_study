import os.path
import time

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
import os,time,random

class ImageStorage(FileSystemStorage):

    def __init__(self,location=settings.MEDIA_ROOT,base_url=settings.MEDIA_URL):
        #初始化
        super(ImageStorage,self).__init__(location,base_url)

    #重写_save方法
    def _save(self, name, content):
        #name=上传文件名称
        ext=os.path.splitext(name)[1]
        #文件目录
        d=os.path.dirname(name)
        #定义文件名,年月日时分秒随机数
        fn=time.strftime('%Y%m%d%H%M%S')
        fn=fn+'_%d'%random.randint(0,100)
        #重写合成方法
        name=os.path.join(d,fn+ext)
        return super(ImageStorage,self)._save(name,content)
