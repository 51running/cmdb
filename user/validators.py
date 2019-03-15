#encoding:utf-8

from .models import User
from datetime import datetime

class Validator(object):
    @classmethod
    def is_interger(cls,value):
        try:
            int(value)
            return True
        except BaseException as e:
            return False

class User_Valid(Validator):   #这里都是view.py在调用的

    @classmethod
    def vaction_login(cls, name, password):
        user = None
        try:
            user = User.objects.get(name=name)
        except BaseException as e:
            pass
        if user is None:
            return None
        if user.password == password:
            return user

    @classmethod
    def valid_insert_user(cls,params):
        is_valid = True
        user = User()
        errors = {}
        users = User.objects.all()
        user.name = params.get('name', '').strip()
        print(params.get('tel', '0'))
        for cuser in users: # cuser是一个类的实例可以直接通过.name访问
            if cuser.name == user.name:
                errors['name'] = '用户名已存在'
                is_valid = False
                break
        user.age = params.get('age', '0').strip()
        if not cls.is_interger(user.age):
        # if not user.age.isdigit():
            errors['age']  = '年龄格式错误'
            is_valid = False
        else:
            user.age = int(user.age)
        user.sex = int(params.get('sex', '0'))   #文件列表sex的值是整型，要不是整型，性别都为男
        user.tel = params.get('tel', '0')
        user.password = params.get('password', '123456')
        user.create_time = datetime.now()
        user.addr = 'beijing'
        return is_valid, user, errors

    @classmethod
    def valid_name_unique(cls,name, uid):
        user = None
        try:
            user = User.objects.get(name=name)
        except BaseException as e:
            pass
        if user is None:
            return True
        else:
            return str(user.id) == str(uid)  # 传进来是字符串类型，数据库是

    @classmethod
    def valid_update_user(cls,params):
        print(params.get('tel', '0'))
        is_valid = True
        errors = {}
        user = None
        try:
            user = User.objects.get(pk=params.get('id','').strip())
        except BaseException as e:
            errors['id'] = '用户信息不存在'
            is_valid = False
            return is_valid, user, errors

        name = params.get('name', '').strip()
        if not cls.valid_name_unique(name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False
        else:
            user.name = name

        age = params.get('age', '0').strip()
        if not age.isdigit():
            errors['age'] = '年龄格式错误'
            is_valid = False
        else:
            user.age = int(age)
        user.sex = int(params.get('sex', '0'))  # w文件列表sex的值是整型，要不是整型，性别都为男
        user.tel = params.get('tel', '0')
        return is_valid, user, errors

    @classmethod
    def valid_find_user(cls,params):
        is_valid = False
        user = User()
        errors = {}
        users = User.objects.all()
        user.name = params.get('name', '').strip()
        for cuser in users:
            if cuser.name == user.name:
                user.id = cuser.id
                is_valid = True
                return is_valid, user, errors
        errors['name'] = '用户名不存在'
        return is_valid, user, errors

    @classmethod
    # def valid_passwd_user(cls,params, id):
    def valid_passwd_user(cls,params, uid):
        is_valid = True
        errors = {}
        user = User.objects.get(pk=uid)
        # user = User(id=result[0]., name=result[1], password=result[2], age=result[3], sex=result[4], tel=result[5])
        user.name = params.get('name', '')
        if params.get('old_passwd') != user.password:  # 此时'id'，json.loads里面的id，没有通过字典推到式，所以id还是字符串
            errors['old_passwd'] = '原密码错误，请重新输入'
            is_valid = False
            return is_valid, user, errors
        if params.get('new_passwd_one') != params.get('new_passwd_two'):
            errors['new_passwd'] = '两次密码输入不一样'
            is_valid = False
            return is_valid, user, errors
        user.password = params.get('new_passwd_two')
        return is_valid, user, errors
