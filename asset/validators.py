#encoding:utf-8

from .models import Host
from datetime import datetime

class Validator(object):
    @classmethod
    def is_interger(cls,value):
        try:
            int(value)
            return True
        except BaseException as e:
            return False

class Host_Valid(Validator):   #这里都是view.py在调用的

    @classmethod
    def valid_update_asset(cls,params):
        is_valid = True
        errors = {}
        host = None
        try:
            host = Host.objects.get(pk=params.get('id','').strip())
        except BaseException as e:
            errors['id'] = '主机信息不存在'
            is_valid = False
            return is_valid, host, errors
        print(host.cpu)
        # return is_valid, host, errors
        name = params.get('name', '').strip()
        if not cls.valid_name_unique(name, host.id):
            errors['name'] = '主机名已存在'
            is_valid = False
        else:
            host.name = name

        ip = params.get('ip', '0').strip()
        host.ip = ip
        # if not ip.isdigit():
        #     errors['ip'] = 'IP格式错误'
        #     is_valid = False
        # else:
        #     host.ip = int(ip)
        host.mac = int(params.get('mac', '0'))  # w文件列表sex的值是整型，要不是整型，性别都为男
        host.os = params.get('os', '0')
        host.arch = params.get('arch', '0')
        host.mem = params.get('mem', '0')
        host.cpu = params.get('cpu', '0')
        host.disk = params.get('disk', '0')
        host.create_time = params.get('create_time', '0')
        host.last_time = params.get('last_time', '0')
        return is_valid, host, errors

    @classmethod
    def valid_name_unique(cls,name, uid):
        host = None
        try:
            host = Host.objects.get(name=name)
        except BaseException as e:
            pass
        if host is None:
            return True
        else:
            return str(host.id) == str(uid)  # 传进来是字符串类型，数据库是
