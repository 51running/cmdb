#encoding:utf-8
import os
import json
import time
from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand
from webanalysis.models import Accesslog

class Command(BaseCommand):
    def handle(self, *args,**options):
        path = os.path.join(settings.BASE_DIR,'media','notices')
        while True:
            lists = os.listdir(path)
            for filename in lists:
                notice = None
                path_notice = os.path.join(path,filename)
                with open(path_notice,'rt') as fhandler:
                    notice = json.loads(fhandler.read())
                try:
                    self.parse(notice)  #防止处理文件不是我们想要的格式
                except BaseException as e:
                    pass
                os.unlink(path_notice)
            time.sleep(5)

    def parse(self,notice):
        file_id = notice['id']  #获取文件里面的id
        path = notice['path']   #获取文件里面的path

        with open(path,'rt') as fhandler:  #这里读的是日志文件
            for line in fhandler:
                try:
                    nodes = line.split()
                    log = Accesslog()   #获取一个对象
                    log.file_id = file_id
                    log.access_time = datetime.strptime(nodes[3],'[%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    log.ip = nodes[0]
                    log.url = nodes[6]
                    log.status_code =nodes[8]
                    log.save()
                except BaseException as e:
                    print(e)
                    print(line)
                print('parse over: {0}'.format(path))
