from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import timedelta
from .models import Host,Resource
from .validators import Host_Valid


def index(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    results = [host.as_dict() for host in Host.objects.all()]
    return render(request,'asset/index.html',{
        'results':results
    })

def list_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    result = [host.as_dict() for host in Host.objects.all()]
    return JsonResponse({'code':200,'result':result})

def view_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    uid = request.GET.get('uid', '')
    # return JsonResponse({
    #     'id': Host.objects.get(pk=uid).id, 'name': Host.objects.get(pk=uid).name, 'ip': Host.objects.get(pk=uid).ip,
    #      'os': Host.objects.get(pk=uid).os,'arch': Host.objects.get(pk=uid).arch,
    #     'mem': Host.objects.get(pk=uid).mem, 'cpu': Host.objects.get(pk=uid).cpu,  # 返回的结果User object (17)，不是Json格式
    #     'disk': Host.objects.get(pk=uid).mem, 'create_time': Host.objects.get(pk=uid).create_time,  # 返回的结果User object (17)，不是Json格式
    #     'last_time': Host.objects.get(pk=uid).last_time
    #      })  # 返回的结果User object (17)，不是Json格式
    host = Host.objects.get(pk=uid)
    return JsonResponse({'code': 200, 'result': host.as_dict()})

def update_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    # print(request.POST.get('id'))
    is_valid , host, errors = Host_Valid.valid_update_asset(request.POST)
    # print(is_valid)
    if is_valid:
        host.save()  # host，host.name、host.age获取name和age所以可以创建一个实例的函数通过self.name去获取name
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code': 400, 'error': errors})

def delete_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})
    uid = request.GET.get('uid','')
    Host.delete_asset(uid)
    return JsonResponse({'code': 200})

def resource_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403})

    uid = request.GET.get('uid', '')
    ip = Host.objects.get(pk=uid).ip
    end_time = timezone.now()
    start_time = end_time - timedelta(hours=1)
    resources = Resource.objects.filter(created_time__gte=start_time,ip=ip).order_by('created_time')

    tmp_resources = {}
    for resource in resources:
        tmp_resources[resource.created_time.strftime('%Y-%m-%d %H:%M')] = {'cpu':resource.cpu,'mem':resource.mem}

    xAxis = []
    CPU_data = []
    MEM_data = []

    while start_time <= end_time:
        key = start_time.strftime('%Y-%m-%d %H:%M')
        resource = tmp_resources.get(key,{})
        xAxis.append(key)
        CPU_data.append(resource.get('cpu',0))
        MEM_data.append(resource.get('mem',0))
        start_time += timedelta(minutes=1)
    print(CPU_data)

    # for resource in resources:
    #     xAxis.append(resource.created_time) #要和echarts的长度的要对应
    #     CPU_data.append(resource.cpu)
    #     MEM_data.append(resource.mem)


    return JsonResponse({'code': 200,'result':{'xAxis':xAxis,'CPU_data':CPU_data,'MEM_data':MEM_data}})