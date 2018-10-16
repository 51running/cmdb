import os
import json
import time
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from webanalysis.models import AccessLogFile,Accesslog

def login_required(func):   #定义一个装饰器，无需添加url，添加@即可调用
    def wrapper(request,*args,**kwargs):
        if request.session.get('user') is None:
            if request.is_ajax():
                return JsonResponse({'code':403,'result':[]})
            return redirect('user:login')

        return func(request, *args,**kwargs)

    return wrapper

@login_required #装饰器，无需添加url，直接调用login_required
def index(request):
    files = AccessLogFile.objects.filter(status=0).order_by('-created_time')[:10]
    return render(request,'webanalysis/index.html',{'files':files})

def upload(request):
    log = request.FILES.get('log')
    # print('name:',log.name,"size:",log.size,"type:",log.content_type)
    if log:
        path = os.path.join(settings.BASE_DIR,'media','uploads',str(time.time()))
        fhandler = open(path,"wb")

        for chunk in log.chunks():
            fhandler.write(chunk)
        fhandler.close()

        obj = AccessLogFile(name=log.name,path=path)
        obj.save()
        path = os.path.join(settings.BASE_DIR,'media','notices',str(time.time()))   #主要用于找路径和id对应关系
        with open(path,'w') as fhandler:
            fhandler.write(json.dumps({'id':obj.id,'path':obj.path}))

    return HttpResponse("上传成功")


@login_required
def dist_status_code(request):
    legend, series = Accesslog.dist_status_code(request.GET.get('id', 0))
    return JsonResponse({'code':200, 'result': {'legend':legend,'series':series}})


@login_required
def trend_visit(request):
    xAxis, series = Accesslog.trend_visit(request.GET.get('id',0))
    print(xAxis,series)
    return JsonResponse({"code":200, "result":{"xAxis":xAxis, "series":series}})