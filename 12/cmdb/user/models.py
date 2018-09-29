#encoding:utf-8

from django.db import models
from .dbuntils import MysqlConnect
import hashlib

def encrypt_password(password):
    if not isinstance(password,bytes):
        password = str(password).encode()
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()


class User(models.Model):
    name = models.CharField(max_length=32, null=False, default='') # name varchar(32) not null defalut=''
    password = models.CharField(max_length=512,null=False, default='')
    age = models.IntegerField(null=False,default=0)
    sex = models.BooleanField(null=False,default=True)
    tel = models.CharField(max_length=32,null=False,default='')
    create_time = models.DateTimeField(null=False)
    addr = models.CharField(max_length=32,null=False,default='')


    @classmethod
    def delete_user(cls,uid):
        return cls.objects.filter(id=uid).delete()


    def as_dict(self):  # 这没有id=None,name=''...，只是说明没有默认值，没有说参数传不进来
        return {'id':self.id, 'name':self.name, 'age':self.age, 'sex':self.sex, 'tel':self.tel}

    @classmethod
    def get_nginx_log(cls):
        cnt, result = MysqlConnect.excute_sql(
            'select ip,time,url,status,count(*) from nginx_log group by ip,time,url,status order by count(*) desc limit 10')
        return cnt, result
