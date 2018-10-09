#encoding: utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse

from .models import get_users,delete_user,get_user,valid_update_user,update_user,valid_insert_user,insert_user,valid_find_user,find_user,valid_passwd_user,get_nginx_log
# from .models import vaction_login
from .models import User
import time

def index(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request, 'user/index.html', {
        'users':User.get_users()
    })

def login(request):
    return render(request, 'user/login.html')

def valid_login(request):
    name = request.POST.get('name')
    password = request.POST.get('password')
    user = User.vaction_login(name,password)
    print(type(user),user)
    user = User.as_dict(user)
    print(type(user), user)
    if user:
        request.session['user'] = user
        return redirect('/user/index/')
    else:
        return render(request, 'user/login.html',{
            'name':name,
            'errors':{'defalut':'用户名或密码错误'}
        })

def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def delete(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    uid = request.GET.get('uid','')
    User.delete_user(uid)
    return redirect('/user/index/')

def view(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    uid = request.GET.get('uid', '')
    return render(request,'user/view.html',{
        'user':User.get_user(uid)
    })

def update(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    is_valid , user, errors = User.valid_update_user(request.POST)
    if is_valid:
        # update_user(user)
        user.update_user()  # user是一个对象，可以通过user.name、user.age获取name和age所以可以创建一个实例的函数通过self.name去获取name
        return redirect('/user/index/')
    else:
        return render(request, 'user/view.html',{
           'user':user,
            'errors':errors
        })

def insert_view(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request,'user/insert_view.html')

def insert(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    is_valid, user, errors = User.valid_insert_user(request.POST)
    if is_valid:
        user.insert_user()
        return redirect('/user/index/')
    else:
        return render(request, 'user/insert_view.html',{
           'user':user,
            'errors':errors
        })

def find_view(request): #这个函数主要是添加一个新的页面
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request,'user/find_view.html')

def find(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    is_valid, user, errors = valid_find_user(request.POST)
    if is_valid:
        finduser = find_user(user)
        return render(request, 'user/find_user_list.html', {
            'user':finduser
        })
    else:
        return render(request, 'user/find_view.html',{
            'user':user,
            'errors':errors
        } )

def passwd_view(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request, 'user/passwd_view.html', {
        'user':request.session['user']
    })

def passwd(request):
    if not request.session.get('user'):
        return redirect('/user/login/')

    is_valid, user, errors = valid_passwd_user(request.POST,request.session.get('user')['id'])
    if is_valid:
        return redirect('/user/index/')
    else:
        return render(request, 'user/passwd_view.html', {
            'user':user,
            'errors':errors
        })

def nginx_log(request):
    cnt, result = get_nginx_log()
    return render(request,'user/nginx_log_view.html',{
            'results':result #这里是一个元组，元组里面有多个元组
    })









