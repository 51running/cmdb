import json
from django.db import models
# from .dbuntils import excute_sql
from .dbuntils import MysqlConnect

sql_list_column = ('id','name','age','sex','tel')

class User(object):

    sql_list_column = ('id', 'name', 'age', 'sex', 'tel')

    def __init__(self, id=None, name='', password='', age=0, sex=1, tel=''):    # 有这些id=None,name=''，只是说明了定义了参数的默认值，不是说在这里定义了这几个参数
        self.id = id
        self.name = name
        self.password = password
        self.age = age
        self.sex = sex
        self.tel = tel

    @classmethod
    def vaction_login(cls, name, password):
        cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user where name=%s and password=%s',(name,password),one=True)
        return User(id=result[0], name=result[1], age=result[2], sex=result[3], tel=result[4]) if result else None  #返回的是一个实例
        # return dict(zip(sql_list_column,result)) if result else None


    @classmethod
    def get_users(cls):
        cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user')
        return [User(id=result[0], name=result[1], age=result[2], sex=result[3], tel=result[4]) for line in result] # []表示一直append增加用户信息
        # return [dict(zip(sql_list_column, line)) for line in result


    @classmethod
    def get_user(cls,uid):
        cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user where id=%s', (uid,), one=True)
        return User(id=result[0], name=result[1], age=result[2], sex=result[3], tel=result[4]) if result else None
        # return user  # 返回key和values


    @classmethod
    def valid_update_user(cls,params):
        is_valid = True
        user = User()   #在类的内部实例一个对象
        errors = {}
        user.id = params.get('id', '').strip()
        if get_user(user.id) is None:
            errors['id'] = '用户信息不存在'
            is_valid = False
        user.name = params.get('name', '').strip()
        if not valid_name_unique(user.name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False
        user.age = params.get('age', '0').strip()
        if not user.age.isdigit():
            errors['age'] = '年龄格式错误'
            is_valid = False

        user.sex = int(params.get('sex', '0'))  # w文件列表sex的值是整型，要不是整型，性别都为男
        user.tel = params.get('tel', '0')
        return is_valid, user, errors

    def update_user(self):
        nt, result = MysqlConnect.excute_sql('update user set name = %s,age=%s,sex=%s,tel=%s where id=%s ', (
            self.name, self.age, self.sex, self.tel, self.id), fetch=False)
        return True

    @classmethod
    def delete_user(cls,uid):
        cnt, result = MysqlConnect.excute_sql('delete from user where id=%s', (uid,), fetch=False)
        return True


    def as_dict(self):  # 这没有id=None,name=''...，只是说明没有默认值，没有说参数传不进来
        return {'id':self.id, 'name':self.name, 'age':self.age, 'sex':self.sex, 'tel':self.tel}

    @classmethod
    def valid_insert_user(cls,params):
        is_valid = True
        user = User()
        errors = {}
        users = cls.get_users()
        user.name = params.get('name', '').strip()
        print(users)
        for cuser in users:
            if cuser['name'] == user['name']:
                errors['name'] = '用户名已存在'
                is_valid = False
                break
        user.age = params.get('age', '0').strip()
        if not user.age.isdigit():
            errors['age']  = '年龄格式错误'
            is_valid = False

        user.sex = int(params.get('sex', '0'))   #文件列表sex的值是整型，要不是整型，性别都为男
        user.tel = params.get('tel', '0')
        user.password = params.get('password', '123456')
        return is_valid, user, errors

    def insert_user(self):
        cnt, result = MysqlConnect.excute_sql('insert into user(name,password,age,sex,tel) values(%s,%s,%s,%s,%s) ',(self.name,self.password,self.age,self.sex,self.tel), fetch=False)
        return True






def get_users():
    cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user')
    return [dict(zip(sql_list_column,line)) for line in result]



def delete_user(uid):
    cnt, result = MysqlConnect.excute_sql('delete from user where id=%s',(uid,),fetch=False)
    return True


def get_user(uid):
    cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user where id=%s',(uid,),one=True)
    user = dict(zip(sql_list_column,result )) if result else None
    return user   #返回key和values


def get_user_by_name(name):
    cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user where name=%s',(name,),one=True)
    user = dict(zip(sql_list_column,result )) if result else None
    return user   #返回key和values


def valid_name_unique(name,uid):
    user = get_user_by_name(name)
    if user is None:
        return True
    else:
        return str(user['id']) == str(uid)  #传进来是字符串类型，数据库是整型


def valid_update_user(params):
    is_valid = True
    user = {}
    errors = {}
    # users = get_users()
    user['id'] =  params.get('id', '').strip()
    if get_user(user['id']) is None:
        errors['id'] = '用户信息不存在'
        is_valid = False
    user['name'] = params.get('name', '').strip()
    if not valid_name_unique(user['name'],user['id']):
            errors['name'] = '用户名已存在'
            is_valid = False
    user['age'] = params.get('age', '0').strip()
    if not user['age'].isdigit():
        errors['age']  = '年龄格式错误'
        is_valid = False

    user['sex'] = int(params.get('sex', '0'))   #w文件列表sex的值是整型，要不是整型，性别都为男
    user['tel'] = params.get('tel', '0')
    return is_valid, user, errors

def update_user(params):
    nt, result = MysqlConnect.excute_sql('update user set name = %s,age=%s,sex=%s,tel=%s where id=%s ',(params['name'],params['age'],params['sex'],params['tel'],params['id']), fetch=False)
    return  True


def valid_insert_user(params):
    is_valid = True
    user = {}
    errors = {}
    users = get_users()
    user['name'] = params.get('name', '').strip()
    for cuser in users:
        if cuser['name'] == user['name']:
            errors['name'] = '用户名已存在'
            is_valid = False
            break
    user['age'] = params.get('age', '0').strip()
    if not user['age'].isdigit():
        errors['age']  = '年龄格式错误'
        is_valid = False

    user['sex'] = int(params.get('sex', '0'))   #文件列表sex的值是整型，要不是整型，性别都为男
    user['tel'] = params.get('tel', '0')
    user['password'] = params.get('password', '123456')
    return is_valid, user, errors


def insert_user(params):
    cnt, result = MysqlConnect.excute_sql('insert into user(name,password,age,sex,tel) values(%s,%s,%s,%s,%s) ',(params['name'],params['password'],params['age'],params['sex'],params['tel']), fetch=False)
    return True


def valid_find_user(params):
    is_valid = False
    user = {}
    errors = {}
    users = get_users()
    user['name'] = params.get('name', '').strip()
    for cuser in users:
        if cuser['name'] == user['name']:
            user['id'] = cuser['id']
            is_valid = True
            return is_valid, user, errors
    errors['name'] = '用户名不存在'
    return is_valid, user, errors


def find_user(params):
    cnt, result = MysqlConnect.excute_sql('select id,name,age,sex,tel from user where id = %s',(params['id'],), one=True)
    finduser = dict(zip(('id','name','age','sex','tel'), result))
    return finduser #返回的是字典


def valid_passwd_user(params,id):
    is_valid = True
    user = {}
    errors = {}
    cnt, result = MysqlConnect.excute_sql('select id,name,password,age,sex,tel from user where id = %s',(id,), one=True)
    users = dict(zip(('id', 'name', 'password','age', 'sex', 'tel'), result))
    user['name'] = params.get('name','')
    if params.get('old_passwd') != users['password']:   #此时'id'，json.loads里面的id，没有通过字典推到式，所以id还是字符串
        errors['old_passwd'] = '原密码错误，请重新输入'
        is_valid = False
        return is_valid, user, errors
    if params.get('new_passwd_one') != params.get('new_passwd_two'):
        errors['new_passwd'] = '两次密码输入不一样'
        is_valid = False
        return is_valid, user, errors
    cnt, result = MysqlConnect.excute_sql('update user set password = %s where id = %s', (params.get('new_passwd_two'),id), fetch=False)
    return is_valid, user, errors

def get_nginx_log():
    cnt, result = MysqlConnect.excute_sql('select ip,time,url,status,count(*) from nginx_log group by ip,time,url,status order by count(*) desc limit 10')
    return cnt, result






