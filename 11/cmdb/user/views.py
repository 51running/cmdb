#encoding: utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse


from .models import User,encrypt_password
from .validators import User_Valid
import time

def index(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request, 'user/index.html', {
        'users':User.objects.all()
    })

def login(request):
    return render(request, 'user/login.html')

def valid_login(request):
    name = request.POST.get('name')
    password = request.POST.get('password')
    password = encrypt_password(password)
    print(password)
    user = User_Valid.vaction_login(name,password)
    if user:
        request.session['user'] =user.as_dict()
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

def delete_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    uid = request.GET.get('uid','')
    User.delete_user(uid)
    return JsonResponse({'code': 200})



def view(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    uid = request.GET.get('uid', '')
    return render(request,'user/view.html',{
        'user':User.objects.get(pk=uid)
    })

def view_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    uid = request.GET.get('uid', '')
    # user = User.objects.get(pk=uid)
    # return JsonResponse({'user':User.objects.get(pk=uid)})  # 返回的结果User object (17)，不是Json格式
    return JsonResponse({'id':User.objects.get(pk=uid).id,'name':User.objects.get(pk=uid).name,'age':User.objects.get(pk=uid).age,'tel':User.objects.get(pk=uid).tel,'tel':User.objects.get(pk=uid).tel,'sex':User.objects.get(pk=uid).sex})  # 返回的结果User object (17)，不是Json格式

    # return render(request,'user/view.html',{
    #     'user':User.objects.get(pk=uid)
    # })

def update(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    is_valid , user, errors = User_Valid.valid_update_user(request.POST)
    if is_valid:
        user.save()  # user是一个对象，可以通过user.name、user.age获取name和age所以可以创建一个实例的函数通过self.name去获取name
        return redirect('/user/index/')
    else:
        return render(request, 'user/view.html',{
           'user':user,
            'errors':errors
        })

def update_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    # print(request.POST.get('tel'))
    is_valid , user, errors = User_Valid.valid_update_user(request.POST)
    print(is_valid)
    if is_valid:
        user.save()  # user是一个对象，可以通过user.name、user.age获取name和age所以可以创建一个实例的函数通过self.name去获取name
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code': 400, 'error': errors})


def insert_view(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request,'user/insert_view.html')

def insert(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    is_valid, user, errors = User_Valid.valid_insert_user(request.POST)
    user.password = encrypt_password(user.password) #md5密码
    if is_valid:
        user.save()
        return redirect('/user/index/')
    else:
        return render(request, 'user/insert_view.html',{
           'user':user,
            'errors':errors
        })

def insert_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code':403})
    print(request.POST)
    is_valid, user, errors = User_Valid.valid_insert_user(request.POST)
    user.password = encrypt_password(user.password)
    if is_valid:
        user.save()
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code':400,'error':errors})



def find_view(request): #这个函数主要是添加一个新的页面
    if not request.session.get('user'):
        return redirect('/user/login/')
    return render(request,'user/find_view.html')

def find(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    is_valid, user, errors = User_Valid.valid_find_user(request.POST)
    if is_valid:
        # finduser = user.find_user()
        return render(request, 'user/find_user_list.html', {
            'user':User.objects.get(id=user.id)
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

    is_valid, user, errors  = User_Valid.valid_passwd_user(request.POST,request.session.get('user')['id'])
    user.password = encrypt_password(user.password)
    if is_valid:
        # user.update_password(request.session.get('user')['id'])
        user.save()
        return redirect('/user/index/')
    else:
        return render(request, 'user/passwd_view.html', {
            'user':user,
            'errors':errors
        })

def nginx_log(request):
    cnt, result = User.get_nginx_log()
    return render(request,'user/nginx_log_view.html',{
            'results':result #这里是一个元组，元组里面有多个元组
    })

